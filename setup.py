from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = f.read()

with open('requirements-tests.txt', 'r') as f:
    test_requirements = f.read()

setup(
    name='aws_lambda_logging',
    description='Nanolib to enhance logging in aws lambda',
    py_modules=['aws_lambda_logging'],
    install_requires=requirements,
    tests_require=test_requirements,
)
