==================
AWS Lambda Logging
==================

.. image:: https://gitlab.com/hadrien/aws_lambda_logging/badges/master/build.svg

.. image:: https://gitlab.com/hadrien/aws_lambda_logging/badges/master/coverage.svg?job=Run%20py.test

Better logging for aws lambda running on python runtime environment with a
highly opinionated JSON formatting to ease parsing on any logging system.

Usage
=====

.. code::

    import aws_lambda_logging


    def handler(event, context):
        aws_lambda_logging.setup(level='DEBUG')
        ...

You can separately set the logging level for Boto (defaults to the same level):

.. code::

    import aws_lambda_logging


    def handler(event, context):
        aws_lambda_logging.setup(level='DEBUG', boto_level='CRITICAL')
        ...



You can add keyword arguments to be logged each time, such as lambda request
id.

.. code::

    import aws_lambda_logging


    def handler(event, context):
        aws_lambda_logging.setup(level='DEBUG',
                                 aws_request_id=context.get('aws_request_id'))
        log.debug('Just a try!')
        ...


It will output JSON formatted message:

.. code::

    {
        "level": "DEBUG",
        "timestamp": "2016-10-03 13:27:57,438",
        "apigw_request_id": "323fee86-896d-11e6-b7fd-2d914ea80962",
        "location": "root.handler:6",
        "message": "Just a try!"
    }

You can input a JSON string:
.. code::
        ...
        log.debug("{"Details": [1,2,3]}")
        ...

It will output JSON formatted message with the JSON string embedded properly:

.. code::

    {
        "level": "DEBUG",
        "timestamp": "2016-10-03 13:27:57,438",
        "apigw_request_id": "323fee86-896d-11e6-b7fd-2d914ea80962",
        "location": "root.handler:6",
        "message": {
            "Details": [
                1,
                2,
                3
            ]
        }
    }
