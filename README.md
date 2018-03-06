# IBM Cloud Object Storage - Python SDK

This package allows Python developers to write software that interacts with [IBM
Cloud Object Storage](https://console.bluemix.net/docs/services/cloud-object-storage/about-cos.html).  It is a fork of [the ``boto3`` library](https://github.com/boto/boto3) and can stand as a drop-in replacement if the application needs to connect to object storage using an S3-like API and does not make use of other AWS services.

## Documentation

* [Core documentation for IBM COS](https://console.bluemix.net/docs/services/cloud-object-storage/getting-started.html)
* [Python API reference documentation](https://ibm.github.io/ibm-cos-sdk-python)
* [REST API reference documentation](https://console.bluemix.net/docs/services/cloud-object-storage/api-reference/about-compatibility-api.html)

For release notes, see the [CHANGELOG](CHANGELOG.md).

* [Example code](#example-code)
* [Building from source](#building-from-source)
* [Getting help](#getting-help)

## Quick start

You'll need:
  * An instance of COS.
  * An API key from [IBM Cloud Identity and Access Management](https://console.bluemix.net/docs/iam/users_roles.html) with at least `Writer` permissions.
  * The ID of the instance of COS that you are working with.
  * Token acquisition endpoint
  * Service endpoint

These values can be found in the Bluemix UI by [generating a 'service credential'](https://console.bluemix.net/docs/services/cloud-object-storage/iam/service-credentials.html).


## Getting the SDK
Install the library from PyPi using `pip`:

```sh
$ pip install ibm-cos-sdk
```

## Deprecation Notice

Deprecation Notice for IBM Cloud Object Storage Java and Python SDK Versions 1.x

As of March 31, 2018, IBM will no longer add new features to the IBM Cloud Object Storage Java SDK Versions 1.x and the IBM Cloud Object Storage Python SDK Versions 1.x.  We will continue to provide critical bug fixes to the 1.x releases through May 31, 2018.

Versions 1.x for Java and Python SDK will no longer be supported after May 31, 2018.

If you are using the 1.x version of the Java or Python SDK, please upgrade to the latest IBM Cloud Object Storage SDK versions 2.x.  Instructions on how to upgrade from SDK Java and Python 1.x can be found in the "Migrating from 1.x.x" section of corresponding Readme.

Note: The IBM Cloud Object Storage Node.js SDK is NOT affected by this change.

For questions, please open an issue:

[Java](https://github.com/ibm/ibm-cos-sdk-java/issues/new)

[Python](https://github.com/ibm/ibm-cos-sdk-python/issues/new)

## Migrating from 1.x.x
The 2.0 release of the SDK introduces a namespacing change that allows an application to make use of the original `boto3` library to connect to AWS resources within the same application or environment.  To migrate from 1.x to 2.0 some changes are necessary.

  1. Update the `requirements.txt`, or from PyPI via `pip install -U ibm-cos-sdk`.  Verify no older versions exist with `pip list | grep ibm-cos`.
  2. Update any import declarations from `boto3` to `ibm_boto3`.
  3. If access to AWS APIs is needed, reinstall the original `boto3` by updating the `requirements.txt`, or from PyPI via `pip install boto3`.

## Example code
Create a file `BucketList.py`, replacing your own values for API key, instance ID, and bucket name:

```python
import boto3
from botocore.client import Config

api_key = 'API_KEY'
service_instance_id = 'RESOURCE_INSTANCE_ID'
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

new_bucket = 'NewBucket'
new_cold_bucket = 'NewColdBucket'

cos = boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

cos.create_bucket(Bucket=new_bucket)

cos.create_bucket(Bucket=new_cold_bucket,
                    CreateBucketConfiguration={
                        'LocationConstraint': 'us-cold'
                    },
)

for bucket in cos.buckets.all():
        print(bucket.name)
```

From the command line, run `python BucketList.py`.  You should see a list of your buckets.

## Building from source

Assuming that you have Python and `virtualenv` installed, set up your
environment and install the required dependencies like this instead of
the `pip install ibm-cos-sdk` defined above:

```sh
$ git clone https://github.com/ibm/ibm-cos-sdk-python.git
$ cd ibm-cos-sdk-python
$ virtualenv venv
...
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
```

## Getting Help

Feel free to use GitHub issues for tracking bugs and feature requests, but for help please use one of the following resources:

* Read a quick start guide in [Bluemix Docs](https://console.bluemix.net/docs/services/cloud-object-storage/libraries/python.html#python).
* Ask a question on [Stack Overflow](https://stackoverflow.com/) and tag it with `ibm` and `object-storage`.
* Open a support ticket with [IBM Bluemix Support](https://support.ng.bluemix.net/gethelp/)
* If it turns out that you may have found a bug, please [open an issue](https://github.com/ibm/ibm-cos-sdk-python/issues/new).

## License

This SDK is distributed under the
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0),
see LICENSE.txt and NOTICE.txt for more information.
