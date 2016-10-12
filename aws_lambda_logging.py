import json
import logging


class JsonFormatter(logging.Formatter):

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
        log_dict = {k: v % record_dict
                    for k, v in self.format_dict.items()
                    if v
                    }
        return json.dumps(log_dict).decode('utf-8')


def setup(level='DEBUG', **kwargs):
    for handler in logging.root.handlers:
        handler.setFormatter(JsonFormatter(**kwargs))

    try:
        logging.root.setLevel(level)
    except ValueError:
        logging.root.setLevel('INFO')
        logging.root.error('Invalid log level: %s', level)
