import io
import json
import logging

from pytest import fixture, yield_fixture
from pytest import mark


@fixture
def stdout():
    return io.StringIO()


@fixture
def handler(stdout):
    return logging.StreamHandler(stdout)


@fixture
def logger():
    return logging.getLogger(__name__)


@yield_fixture
def root_logger(handler):
    logging.root.addHandler(handler)
    yield logging.root
    logging.root.removeHandler(handler)


@mark.parametrize('level', ['DEBUG', 'WARNING', 'ERROR', 'INFO', 'CRITICAL'])
def test_setup_with_valid_log_levels(root_logger, logger, stdout, level):
    from aws_lambda_logging import setup
    setup(level, request_id='request id!', another='value')

    logger.critical('This is a test')

    log_dict = json.loads(stdout.getvalue())

    check_log_dict(log_dict)

    assert 'CRITICAL' == log_dict['level']
    assert 'This is a test' == log_dict['message']
    assert 'request id!' == log_dict['request_id']


def test_setup_with_invalid_log_level(root_logger, logger, stdout):
    from aws_lambda_logging import setup
    setup('not a valid log level', request_id='request id!', another='value')

    log_dict = json.loads(stdout.getvalue())

    check_log_dict(log_dict)


def check_log_dict(log_dict):
    assert 'timestamp' in log_dict
    assert 'level' in log_dict
    assert 'location' in log_dict
    assert 'message' in log_dict
