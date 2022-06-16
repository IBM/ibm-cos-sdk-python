# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License'). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# https://aws.amazon.com/apache2.0/
#
# or in the 'license' file accompanying this file. This file is
# distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import pytest
from ibm_s3transfer.futures import NonThreadedExecutor
from ibm_s3transfer.manager import TransferManager

from ibm_boto3.exceptions import RetriesExceededError, S3UploadFailedError
from ibm_boto3.s3.transfer import (
    KB,
    MB,
    ClientError,
    OSUtils,
    ProgressCallbackInvoker,
    S3Transfer,
    S3TransferRetriesExceededError,
    TransferConfig,
    create_transfer_manager,
)
from tests import mock, unittest


class TestCreateTransferManager(unittest.TestCase):
    def test_create_transfer_manager(self):
        client = object()
        config = TransferConfig()
        osutil = OSUtils()
        with mock.patch('ibm_boto3.s3.transfer.TransferManager') as manager:
            create_transfer_manager(client, config, osutil)
            assert manager.call_args == mock.call(client, config, osutil, None)

    def test_create_transfer_manager_with_no_threads(self):
        client = object()
        config = TransferConfig()
        config.use_threads = False
        with mock.patch('ibm_boto3.s3.transfer.TransferManager') as manager:
            create_transfer_manager(client, config)
            assert manager.call_args == mock.call(
                client, config, None, NonThreadedExecutor
            )


class TestTransferConfig(unittest.TestCase):
    def assert_value_of_actual_and_alias(
        self, config, actual, alias, ref_value
    ):
        # Ensure that the name set in the underlying TransferConfig (i.e.
        # the actual) is the correct value.
        assert getattr(config, actual) == ref_value
        # Ensure that backcompat name (i.e. the alias) is the correct value.
        assert getattr(config, alias) == ref_value

    def test_alias_max_concurreny(self):
        ref_value = 10
        config = TransferConfig(max_concurrency=ref_value)
        self.assert_value_of_actual_and_alias(
            config, 'max_request_concurrency', 'max_concurrency', ref_value
        )

        # Set a new value using the alias
        new_value = 15
        config.max_concurrency = new_value
        # Make sure it sets the value for both the alias and the actual
        # value that will be used in the TransferManager
        self.assert_value_of_actual_and_alias(
            config, 'max_request_concurrency', 'max_concurrency', new_value
        )

    def test_alias_max_io_queue(self):
        ref_value = 10
        config = TransferConfig(max_io_queue=ref_value)
        self.assert_value_of_actual_and_alias(
            config, 'max_io_queue_size', 'max_io_queue', ref_value
        )

        # Set a new value using the alias
        new_value = 15
        config.max_io_queue = new_value
        # Make sure it sets the value for both the alias and the actual
        # value that will be used in the TransferManager
        self.assert_value_of_actual_and_alias(
            config, 'max_io_queue_size', 'max_io_queue', new_value
        )

    def test_transferconfig_parameters(self):
        config = TransferConfig(
            multipart_threshold=8 * MB,
            max_concurrency=10,
            multipart_chunksize=8 * MB,
            num_download_attempts=5,
            max_io_queue=100,
            io_chunksize=256 * KB,
            use_threads=True,
            max_bandwidth=1024 * KB,
        )
        assert config.multipart_threshold == 8 * MB
        assert config.multipart_chunksize == 8 * MB
        assert config.max_request_concurrency == 10
        assert config.num_download_attempts == 5
        assert config.max_io_queue_size == 100
        assert config.io_chunksize == 256 * KB
        assert config.use_threads is True
        assert config.max_bandwidth == 1024 * KB


class TestProgressCallbackInvoker(unittest.TestCase):
    def test_on_progress(self):
        callback = mock.Mock()
        subscriber = ProgressCallbackInvoker(callback)
        subscriber.on_progress(bytes_transferred=1)
        callback.assert_called_with(1)


class TestS3Transfer(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.manager = mock.Mock(TransferManager(self.client))
        self.transfer = S3Transfer(manager=self.manager)
        self.callback = mock.Mock()

    def assert_callback_wrapped_in_subscriber(self, call_args):
        subscribers = call_args[0][4]
        # Make sure only one subscriber was passed in.
        assert len(subscribers) == 1
        subscriber = subscribers[0]
        # Make sure that the subscriber is of the correct type
        assert isinstance(subscriber, ProgressCallbackInvoker)
        # Make sure that the on_progress method() calls out to the wrapped
        # callback by actually invoking it.
        subscriber.on_progress(bytes_transferred=1)
        self.callback.assert_called_with(1)

    def test_upload_file(self):
        extra_args = {'ACL': 'public-read'}
        self.transfer.upload_file(
            'smallfile', 'bucket', 'key', extra_args=extra_args
        )
        self.manager.upload.assert_called_with(
            'smallfile', 'bucket', 'key', extra_args, None
        )

    def test_download_file(self):
        extra_args = {
            'SSECustomerKey': 'foo',
            'SSECustomerAlgorithm': 'AES256',
        }
        self.transfer.download_file(
            'bucket', 'key', '/tmp/smallfile', extra_args=extra_args
        )
        self.manager.download.assert_called_with(
            'bucket', 'key', '/tmp/smallfile', extra_args, None
        )

    def test_upload_wraps_callback(self):
        self.transfer.upload_file(
            'smallfile', 'bucket', 'key', callback=self.callback
        )
        self.assert_callback_wrapped_in_subscriber(
            self.manager.upload.call_args
        )

    def test_download_wraps_callback(self):
        self.transfer.download_file(
            'bucket', 'key', '/tmp/smallfile', callback=self.callback
        )
        self.assert_callback_wrapped_in_subscriber(
            self.manager.download.call_args
        )

    def test_propogation_of_retry_error(self):
        future = mock.Mock()
        future.result.side_effect = S3TransferRetriesExceededError(Exception())
        self.manager.download.return_value = future
        with pytest.raises(RetriesExceededError):
            self.transfer.download_file('bucket', 'key', '/tmp/smallfile')

    def test_propogation_s3_upload_failed_error(self):
        future = mock.Mock()
        future.result.side_effect = ClientError({'Error': {}}, 'op_name')
        self.manager.upload.return_value = future
        with pytest.raises(S3UploadFailedError):
            self.transfer.upload_file('smallfile', 'bucket', 'key')

    def test_can_create_with_just_client(self):
        transfer = S3Transfer(client=mock.Mock())
        assert isinstance(transfer, S3Transfer)

    def test_can_create_with_extra_configurations(self):
        transfer = S3Transfer(
            client=mock.Mock(), config=TransferConfig(), osutil=OSUtils()
        )
        assert isinstance(transfer, S3Transfer)

    def test_client_or_manager_is_required(self):
        with pytest.raises(ValueError):
            S3Transfer()

    def test_client_and_manager_are_mutually_exclusive(self):
        with pytest.raises(ValueError):
            S3Transfer(self.client, manager=self.manager)

    def test_config_and_manager_are_mutually_exclusive(self):
        with pytest.raises(ValueError):
            S3Transfer(config=mock.Mock(), manager=self.manager)

    def test_osutil_and_manager_are_mutually_exclusive(self):
        with pytest.raises(ValueError):
            S3Transfer(osutil=mock.Mock(), manager=self.manager)

    def test_upload_requires_string_filename(self):
        transfer = S3Transfer(client=mock.Mock())
        with pytest.raises(ValueError):
            transfer.upload_file(filename=object(), bucket='foo', key='bar')

    def test_download_requires_string_filename(self):
        transfer = S3Transfer(client=mock.Mock())
        with pytest.raises(ValueError):
            transfer.download_file(bucket='foo', key='bar', filename=object())

    def test_context_manager(self):
        manager = mock.Mock()
        manager.__exit__ = mock.Mock()
        with S3Transfer(manager=manager):
            pass
        # The underlying transfer manager should have had its __exit__
        # called as well.
        assert manager.__exit__.call_args == mock.call(None, None, None)

    def test_context_manager_with_errors(self):
        manager = mock.Mock()
        manager.__exit__ = mock.Mock()
        raised_exception = ValueError()
        with pytest.raises(type(raised_exception)):
            with S3Transfer(manager=manager):
                raise raised_exception
        # The underlying transfer manager should have had its __exit__
        # called as well and pass on the error as well.
        assert manager.__exit__.call_args == mock.call(
            type(raised_exception), raised_exception, mock.ANY
        )
