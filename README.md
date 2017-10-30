# IBM Cloud Object Storage - Python SDK


This package allows Python developers to write software that interacts with IBM
Cloud Object Storage.  It is based on ``boto3`` and can stand as a drop-in replacement.


## Quick Start

You'll need:
  * An instance of COS.
  * An API key from IBM Cloud Identity and Access Management with at least `Writer` permissions.
  * The ID of the instance of COS that you are working with.
  * Token acquisition endpoint
  * Service endpoint

These values can be found in the Bluemix UI by generating a 'service credential'.

First, install the library:

```sh
$ pip install ibm-cos-sdk
```

Next, create a file `BucketList.py`, replacing your own values for API key, instance ID, and bucket name:

```python
import boto3
from botocore.client import Config

api_key = 'API_KEY'
service_instance_id = 'RESOURCE_INSTANCE_ID'
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

new_bucket = 'NewBucket'
new_std_bucket = 'NewSTDBucket'

cos = boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

cos.create_bucket(Bucket=new_bucket)

cos.create_bucket(Bucket=new_std_bucket,
                    CreateBucketConfiguration={
                        'LocationConstraint': 'us-standard'
                    },
)

for bucket in cos.buckets.all():
        print(bucket.name)
```

From the command line, run `python BucketList.py`.  You should see a list of your buckets.

## Development

### Getting Started

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
