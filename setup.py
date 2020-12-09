#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-z0-9.]+)['"]''')


requires = [
    'ibm-cos-sdk-core==2.9.0',
    'ibm-cos-sdk-s3transfer==2.9.0',
    'jmespath>=0.7.1,<1.0.0'
]


def get_version():
    init = open(os.path.join(ROOT, 'ibm_boto3', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='ibm-cos-sdk',
    version=get_version(),
    description='IBM SDK for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
    python_requires='~=3.5',
    install_requires=requires,
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
