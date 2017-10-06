"""Microlibrary to simplify logging in AWS Lambda."""

import json
import logging


class JsonFormatter(logging.Formatter):
    """AWS Lambda Logging formatter."""

    def __init__(self, **kwargs):
        super(JsonFormatter, self).__init__()
        self.format_dict = {
            'timestamp': '%(asctime)s',
            'level': '%(levelname)s',
            'location': '%(name)s.%(funcName)s:%(lineno)d',
            'message': '%(message)s',
        }
        self.format_dict.update(kwargs)

    def format(self, record):
        record_dict = record.__dict__.copy()
        record_dict['asctime'] = self.formatTime(record)
        record_dict['message'] = record.getMessage()

        log_dict = {
            k: v % record_dict
            for k, v in self.format_dict.items()
            if v
        }

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

        json_record = json.dumps(log_dict)

        if hasattr(json_record, 'decode'):  # pragma: no cover
            json_record = json_record.decode('utf-8')

        return json_record


def setup(level='DEBUG', formatter_cls=JsonFormatter,
          boto_level=None, **kwargs):
    """Overall Metadata Formatting."""
    if formatter_cls:
        for handler in logging.root.handlers:
            handler.setFormatter(formatter_cls(**kwargs))

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
