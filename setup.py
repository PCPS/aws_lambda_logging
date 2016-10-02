from setuptools import setup

with open('requirements-tests.txt') as f:
    test_requirements = f.read()

with open('VERSION') as f:
    version = f.read().strip()


setup(
    version=version,
    name='aws_lambda_logging',
    description='Nanolib to enhance logging in aws lambda',
    py_modules=['aws_lambda_logging'],
    tests_require=test_requirements,
)
