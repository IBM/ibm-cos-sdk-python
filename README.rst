IBM Cloud Object Storage - Python SDK
=====================================

This package allows Python developers to write software that interacts
with `IBM Cloud Object
Storage <https://cloud.ibm.com/docs/services/cloud-object-storage/about-cos.html>`__.
It is a fork of the `boto3 library <https://github.com/boto/boto3>`__ 
and can stand as a drop-in replacement if the application needs to connect to object storage using
an S3-like API and does not make use of other AWS services.

Notice
------

IBM is officially deprecating support of Python versions 2.7 & 3.4.   All clients need to upgrade to version 3.5 or greater by January 31, 2020.

Documentation
-------------

-  `Core documentation for IBM
   COS <https://cloud.ibm.com/docs/services/cloud-object-storage/getting-started.html>`__
-  `Python API reference
   documentation <https://ibm.github.io/ibm-cos-sdk-python>`__
-  `REST API reference
   documentation <https://cloud.ibm.com/docs/services/cloud-object-storage/api-reference/about-api.html>`__

For release notes, see the `CHANGELOG <CHANGELOG.md>`__.

-  `Building from source <#building-from-source>`__
-  `Getting help <#getting-help>`__

Quick start
-----------

You'll need: 

-  An instance of COS.
-  An API key from `IBM Cloud Identity and Access Management <https://cloud.ibm.com/docs/iam/users_roles.html>`__ with at least ``Writer`` permissions. 
-  The ID of the instance of COS that you are working with. 
-  Token acquisition endpoint.
-  Service endpoint.

These values can be found in the IBM Cloud Console by `generating a
'service credential' <https://cloud.ibm.com/docs/services/cloud-object-storage/iam/service-credentials.html>`__.

Using Python
------------

Use of the Python SDK and example code can be found
`here <https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#using-python>`__.

Using a Service Credential
--------------------------

You can source credentials directly from a `Service
Credential <https://cloud.ibm.com/docs/services/cloud-object-storage/iam/service-credentials.html>`__
JSON document generated in the IBM Cloud console saved to
``~/.bluemix/cos_credentials``. The SDK will automatically load these
providing you have not explicitly set other credentials during client
creation. If the Service Credential contain `HMAC
keys <https://cloud.ibm.com/docs/services/cloud-object-storage/hmac/credentials.html>`__
the client will use those and authenticate using a signature, otherwise
the client will use the provided API key to authenticate using bearer
tokens.

Aspera high-speed transfer
--------------------------

It is now possible to use the IBM Aspera high-speed transfer service as
an alternative method to managed transfers of larger objects. The Aspera
high-speed transfer service is especially effective across long
distances or in environments with high rates of packet loss. For more
details, check out the `IBM Cloud
documentation <https://cloud.ibm.com/docs/services/cloud-object-storage/basics/aspera.html#using-libraries-and-sdks>`__.

Archive Tier Support
--------------------

You can automatically archive objects after a specified length of time
or after a specified date. Once archived, a temporary copy of an object
can be restored for access as needed. Restore time may take up to 15
hours.

An archive policy is set at the bucket level by calling the
``put_bucket_lifecycle_configuration`` method on a client instance. A
newly added or modified archive policy applies to new objects uploaded
and does not affect existing objects. For more detail, `see the
documentation <https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#python>`__.

Immutable Object Storage
------------------------

Users can configure buckets with an Immutable Object Storage policy to
prevent objects from being modified or deleted for a defined period of
time. The retention period can be specified on a per-object basis, or
objects can inherit a default retention period set on the bucket. It is
also possible to set open-ended and permanent retention periods.
Immutable Object Storage meets the rules set forth by the SEC governing
record retention, and IBM Cloud administrators are unable to bypass
these restrictions. For more detail, `see the IBM Cloud
documentation <https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#python>`__.

Note: Immutable Object Storage does not support Aspera transfers via the
SDK to upload objects or directories at this stage.

Building from source
--------------------

Assuming that you have Python and ``virtualenv`` installed, set up your
environment and install the required dependencies like this instead of
the ``pip install ibm-cos-sdk`` defined above:

.. code:: sh

    $ git clone https://github.com/ibm/ibm-cos-sdk-python.git
    $ cd ibm-cos-sdk-python
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ pip install -r requirements.txt
    $ pip install -e .

Getting Help
------------

Feel free to use GitHub issues for tracking bugs and feature requests,
but for help please use one of the following resources:

-  Read a quick start guide in `IBM Cloud
   Docs <https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#python>`__.
-  Ask a question on `Stack Overflow <https://stackoverflow.com/>`__ and
   tag it with ``ibm`` and ``object-storage``.
-  Open a support ticket with `IBM Cloud
   Support <https://cloud.ibm.com/unifiedsupport/supportcenter/>`__
-  If it turns out that you may have found a bug, please `open an
   issue <https://github.com/ibm/ibm-cos-sdk-python/issues/new>`__.

License
-------

This SDK is distributed under the `Apache License, Version
2.0 <http://www.apache.org/licenses/LICENSE-2.0>`__, see LICENSE.txt and
NOTICE.txt for more information.
