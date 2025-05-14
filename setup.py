#!/usr/bin/env python
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-z0-9.]+)['"]''')


requires = [
    'ibm-cos-sdk-core==2.14.1',
    'ibm-cos-sdk-s3transfer==2.14.1',
    'jmespath>=0.10.0,<=1.0.1'
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
    package_data={'ibm_boto3': ['data/aws/resources/*.json', 'examples/*.rst']},
    include_package_data=True,
    install_requires=requires,
    license="Apache License 2.0",
    python_requires=">= 3.8",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    project_urls={
        'Documentation': 'https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-python',
        'Source': 'https://github.com/IBM/ibm-cos-sdk-python',
    },
)
