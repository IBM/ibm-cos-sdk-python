# IBM Cloud Object Storage - Python SDK

This package allows Python developers to write software that interacts with [IBM Cloud Object Storage](https://cloud.ibm.com/docs/services/cloud-object-storage/about-cos.html). It is a fork of the [`boto3` library](https://github.com/boto/boto3) and can stand as a drop-in replacement if the application needs to connect to object storage using an S3-like API and does not make use of other AWS services.

## Notice

IBM has added a [Language Support Policy](#language-support-policy). Language versions will be deprecated on the published schedule without additional notice.

## Documentation

* [Core documentation for IBM COS](https://cloud.ibm.com/docs/services/cloud-object-storage/getting-started.html)
* [Python API reference documentation](https://ibm.github.io/ibm-cos-sdk-python)
* [REST API reference documentation](https://cloud.ibm.com/docs/services/cloud-object-storage/api-reference/about-api.html)

For release notes, see the [CHANGELOG](CHANGELOG.md).

* [Building from Source](#building-from-source)
* [Getting Help](#getting-help)

## Quick start

You\'ll need:

* An instance of COS.
* An API key from [IBM Cloud Identity and Access Management](https://cloud.ibm.com/docs/iam/users_roles.html) with at least `Writer` permissions.
* The ID of the instance of COS that you are working with.
* Token acquisition endpoint.
* Service endpoint.

These values can be found in the IBM Cloud Console by [generating a \'service credential\'](https://cloud.ibm.com/docs/services/cloud-object-storage/iam/service-credentials.html).

## Using Python

Use of the Python SDK and example code can be found [here](https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#using-python).

## Using a Service Credential

You can source credentials directly from a [Service Credential](https://cloud.ibm.com/docs/services/cloud-object-storage/iam/service-credentials.html) JSON document generated in the IBM Cloud console saved to `~/.bluemix/cos_credentials`. The SDK will automatically load these providing you have not explicitly set other credentials during client creation. If the Service Credential contain [HMAC keys](https://cloud.ibm.com/docs/services/cloud-object-storage/hmac/credentials.html) the client will use those and authenticate using a signature, otherwise the client will use the provided API key to authenticate using bearer tokens.

## Aspera high-speed transfer

It is now possible to use the IBM Aspera high-speed transfer service as an alternative method to managed transfers of larger objects. The Aspera high-speed transfer service is especially effective across long distances or in environments with high rates of packet loss. For more details, check out the [IBM Cloud documentation](https://cloud.ibm.com/docs/services/cloud-object-storage/basics/aspera.html#using-libraries-and-sdks).

## Archive Tier Support

You can automatically archive objects after a specified length of time or after a specified date. Once archived, a temporary copy of an object can be restored for access as needed. Restore time may take up to 15 hours.

An archive policy is set at the bucket level by calling the `put_bucket_lifecycle_configuration` method on a client instance. A newly added or modified archive policy applies to new objects uploaded and does not affect existing objects. For more detail, [see the documentation](https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#python).

## Immutable Object Storage

Users can configure buckets with an Immutable Object Storage policy to prevent objects from being modified or deleted for a defined period of time. The retention period can be specified on a per-object basis, or objects can inherit a default retention period set on the bucket. It is also possible to set open-ended and permanent retention periods. Immutable Object Storage meets the rules set forth by the SEC governing record retention, and IBM Cloud administrators are unable to bypass these restrictions. For more detail, [see the IBM Cloud documentation](https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#python).

Note: Immutable Object Storage does not support Aspera transfers via the SDK to upload objects or directories at this stage.

## Accelerated Archive

Users can set an archive rule that would allow data restore from an archive in 2 hours or 12 hours.

## Building from source

Assuming that you have Python and `virtualenv` installed, set up your environment and install the required dependencies like this instead of the `pip install ibm-cos-sdk` defined above:

```sh
git clone https://github.com/ibm/ibm-cos-sdk-python.git
cd ibm-cos-sdk-python
$ virtualenv venv
...
. venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Getting Help

Feel free to use GitHub issues for tracking bugs and feature requests, but for help please use one of the following resources:

* Read a quick start guide in [IBM Cloud Docs](https://cloud.ibm.com/docs/services/cloud-object-storage/libraries/python.html#python).
* Ask a question on [Stack Overflow](https://stackoverflow.com/) and tag it with `ibm` and `object-storage`.
* Open a support ticket with [IBM Cloud Support](https://cloud.ibm.com/unifiedsupport/supportcenter/)
* If it turns out that you may have found a bug, please [open an issue](https://github.com/ibm/ibm-cos-sdk-python/issues/new).

## Language Support Policy

IBM supports [current public releases](https://devguide.python.org/#status-of-python-branches). IBM will deprecate language versions 90 days after a version reaches end-of-life. All clients will need to upgrade to a supported version before the end of the grace period.

## License

This SDK is distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0), see LICENSE.txt and NOTICE.txt for more information.
