.. _guide_clients:

Low-level Clients
=================
Clients provide a low-level interface to AWS whose methods map close to 1:1
with service APIs. All service operations are supported by clients. Clients
are generated from a JSON service definition file.

Creating Clients
----------------
Clients are created in a similar fashion to resources::

    import boto3

    # Create a low-level client with the service name
    s3 = boto3.client('s3')

It is also possible to access the low-level client from an existing
resource::

    # Create the resource
    s3_resource = boto3.resource('s3')

    # Get the client from the resource
    s3 = s3.meta.client

Service Operations
------------------
Service operations map to client methods of the same name and provide
access to the same operation parameters via keyword arguments::

    # Make a call using the low-level client
    response = s3.put_object(Bucket='...', Metadata={'...'})

As can be seen above, the method arguments map directly to the associated
`S3 API <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html>`_.

.. note::

   The method names have been snake-cased for better looking Python code.

   Parameters **must** be sent as keyword arguments. They will not work
   as positional arguments.

Handling Responses
------------------
Responses are returned as python dictionaries. It is up to you to traverse
or otherwise process the response for the data you need, keeping in mind
that responses may not always include all of the expected data. In the
example below, ``response.get('Buckets', [])`` is used to ensure that a
list is always returned, even when the response has no key ``'Buckets'``::

    # List all your buckets
    response = s3.list_buckets()
    for bucket in response.get('Buckets', []):
        print(bucket)

The ``response`` in the example above looks something like this:

.. code-block:: json

   {
       "Creation Date": datetime.datetime(),
       "Name": "mybucket"
   }

Waiters
-------
Waiters use a client's service operations to poll the status of an AWS resource
and suspend execution until the AWS resource reaches the state that the
waiter is polling for or a failure occurs while polling.
Using clients, you can learn the name of each waiter that a client has access
to::

    import boto3

    s3 = boto3.client('s3')

    # List all of the possible waiters for s3 client
    print("s3 waiters:")
    s3.waiter_names


Note if a client does not have any waiters, it will return an empty list when
accessing its ``waiter_names`` attribute::

    s3 waiters:
    [u'bucket_exists', u'bucket_not_exists', u'object_exists', u'object_not_exists']

Using a client's ``get_waiter()`` method, you can obtain a specific waiter
from its list of possible waiters::

    # Retrieve waiter instance that will wait till a specified
    # S3 bucket exists
    s3_bucket_exists_waiter = s3.get_waiter('bucket_exists')

Then to actually start waiting, you must call the waiter's ``wait()`` method
with the method's appropriate parameters passed in::

    # Begin waiting for the S3 bucket, mybucket, to exist
    s3_bucket_exists_waiter.wait(Bucket='mybucket')
