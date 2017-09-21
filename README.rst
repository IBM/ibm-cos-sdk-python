=====================================
IBM Cloud Object Storage - Python SDK
=====================================

This package allows Python developers to write software that interacts with IBM
Cloud Object Storage.  It is based on ``boto3`` and can stand as a drop-in replacement.


Quick Start
-----------
First, install the library and set a default region:

.. code-block:: sh

    $ pip install ibm-cos-sdk

Next, set up credentials (in e.g. ``~/.aws/credentials``):

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET

Then, set up a default region (in e.g. ``~/.aws/config``):

.. code-block:: ini

    [default]
    region=us-geo

Then, from a Python interpreter:

.. code-block:: python

    >>> import boto3
    >>> cos = boto3.resource('s3')
    >>> for bucket in cos.buckets.all():
            print(bucket.name)

Development
-----------

Getting Started
~~~~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, set up your
environment and install the required dependencies like this instead of
the ``pip install ibm-cos-sdk`` defined above:

.. code-block:: sh

    $ git clone https://github.com/ibm/ibm-cos-sdk-python.git
    $ cd ibm-cos-sdk-python
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ pip install -r requirements.txt
    $ pip install -e .


Getting Help
------------

Feel free to use GitHub issues for tracking bugs and feature requests, but for help please use one of the following resources:

* Ask a question on `Stack Overflow <https://stackoverflow.com/>`__ and tag it with ``ibm`` and ``object-storage``.
* Open a support ticket with `IBM Bluemix Support <https://support.ng.bluemix.net/gethelp/>`__
* If it turns out that you may have found a bug, please `open an issue <https://github.com/ibm/ibm-cos-sdk-python/issues/new>`__
