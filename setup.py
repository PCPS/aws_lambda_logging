from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    version=version,
    name='aws_lambda_logging',
    description='Nanolib to enhance logging in aws lambda',
    long_description=long_description,
    py_modules=['aws_lambda_logging'],
    url='https://gitlab.com/hadr/aws_lambda_logging',
    licence='MIT',
    extras_require={
        'tests': [
            'pylama',
            'pytest',
            'pytest-cov',
            'pytest-runner',
            'tox',
        ],
        'dev': [
            'bumpversion',
            'twine',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
