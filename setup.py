#!/usr/bin/env python
import os
import re
import sys
from setuptools import setup, find_packages

# IbmCos sdk python version check
_valid  =  sys.version_info[:2] == (2, 7) or sys.version_info >= (3,4)
if not _valid:
    sys.exit("Sorry, IBM COS SDK only supports versions 2.7, 3.4, 3.5, 3.6, 3.7 of python.")


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-z0-9.]+)['"]''')


requires = [
    'ibm-cos-sdk-core>=2.0.0,==2.*',
    'ibm-cos-sdk-s3transfer>=2.0.0,==2.*'
]


def get_version():
    init = open(os.path.join(ROOT, 'ibm_boto3', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='ibm-cos-sdk',
    version=get_version(),
    description='IBM SDK for Python',
    long_description=open('README.md').read(),
    author='IBM',
    url='https://github.com/ibm/ibm-cos-sdk-python',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    package_data={
        'ibm_boto3': [
            'data/aws/resources/*.json',
            'examples/*.rst'
        ]
    },
    include_package_data=True,
    install_requires=requires,
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
