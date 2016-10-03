from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

with open(path.join(here, 'requirements-tests.txt')) as f:
    test_requirements = f.read()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    version=version,
    name='aws_lambda_logging',
    description='Nanolib to enhance logging in aws lambda',
    long_description=long_description,
    py_modules=['aws_lambda_logging'],
    tests_require=test_requirements,
    url='https://gitlab.com/hadr/aws_lambda_logging',
    licence='MIT',
)
