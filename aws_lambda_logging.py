"""Microlibrary to simplify logging in AWS Lambda."""
import json
import logging
import os
import sys
from functools import wraps

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it
this.formatter_instance = None


def json_formatter(obj):
    """Formatter for unserialisable values."""
    return str(obj)


class JsonFormatter(logging.Formatter):
    """AWS Lambda Logging formatter.

    Formats the log message as a JSON encoded string.  If the message is a
    dict it will be used directly.  If the message can be parsed as JSON, then
    the parse d value is used in the output record.
    """

    def __init__(self, **kwargs):
        """Return a JsonFormatter instance.

        The `json_default` kwarg is used to specify a formatter for otherwise
        unserialisable values.  It must not throw.  Defaults to a function that
        coerces the value to a string.

        Other kwargs are used to specify log field format strings.
        """
        datefmt = kwargs.pop('datefmt', None)

        super(JsonFormatter, self).__init__(datefmt=datefmt)
        # '%(filename)s %(funcName)s %(name)s %(message)s %(module)s %(lineno)d'
        self.format_dict = {
            'timestamp': '%(asctime)s',
            'level': '%(levelname)s',
            'filename': '%(filename)s',
            'funcName': '%(funcName)s',
            'line': '%(lineno)d'
        }
        self.format_dict.update(kwargs)
        self.default_json_formatter = kwargs.pop(
            'json_default', json_formatter)

    def add_field(self, **kwargs):
        self.format_dict.update(kwargs)

    def format(self, record):
        record_dict = record.__dict__.copy()
        record_dict['asctime'] = self.formatTime(record, self.datefmt)

        log_dict = {
            k: v % record_dict
            for k, v in self.format_dict.items()
            if v
        }

        if isinstance(record_dict['msg'], dict):
            log_dict['message'] = record_dict['msg']
        else:
            log_dict['message'] = record.getMessage()

            # Attempt to decode the message as JSON, if so, merge it with the
            # overall message for clarity.
            try:
                log_dict['message'] = json.loads(log_dict['message'])
            except (TypeError, ValueError):
                pass

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            # from logging.Formatter:format
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            log_dict['exception'] = record.exc_text

        json_record = json.dumps(log_dict, default=self.default_json_formatter)

        if hasattr(json_record, 'decode'):  # pragma: no cover
            json_record = json_record.decode('utf-8')

        return json_record


def setup(level='DEBUG', formatter_cls=JsonFormatter,
          boto_level=None, **kwargs):
    """Overall Metadata Formatting."""
    if formatter_cls:
        this.formatter_instance = formatter_cls(**kwargs)
        for handler in logging.root.handlers:
            handler.setFormatter(this.formatter_instance)

    try:
        logging.root.setLevel(level)
    except ValueError:
        logging.root.error('Invalid log level: %s', level)
        level = 'INFO'
        logging.root.setLevel(level)

    if not boto_level:
        boto_level = level

    try:
        logging.getLogger('boto').setLevel(boto_level)
        logging.getLogger('boto3').setLevel(boto_level)
        logging.getLogger('botocore').setLevel(boto_level)
    except ValueError:
        logging.root.error('Invalid log level: %s', boto_level)


def add_field(**kwargs):
    if this.formatter_instance:
        this.formatter_instance.add_field(**kwargs)


def wrap(lambda_handler):
    """Lambda handler decorator that setup logging when handler is called.

    Adds ``request=context.request_id`` on all log messages.

    From environment variables:
    - ``log_level`` set the global log level (default to ``DEBUG``);
    - ``boto_level`` set boto log level (default to ``WARN``);
    """

    @wraps(lambda_handler)
    def wrapper(event, context):
        try:
            request_id = event['requestContext']['requestId']

        except (TypeError, KeyError):
            request_id = getattr(context, 'aws_request_id', None)

        setup(
            level=os.getenv('log_level', 'DEBUG'),
            aws_request_id=request_id,
            function_name=getattr(context, 'function_name', None),
            function_version=getattr(context, 'function_version', None),
            invoked_function_arn=getattr(context, 'invoked_function_arn', None),
            boto_level=os.getenv('boto_level', 'WARN'),
        )
        return lambda_handler(event, context)

    return wrapper
