# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from ibm_botocore import loaders
from ibm_botocore.exceptions import DataNotFoundError, UnknownServiceError
from ibm_botocore.client import Config

from ibm_boto3 import __version__
from ibm_boto3.exceptions import NoVersionFound, ResourceNotExistsError
from ibm_boto3.session import Session
from tests import mock, BaseTestCase


class TestSession(BaseTestCase):

    def test_repr(self):
        bc_session = self.bc_session_cls.return_value
        bc_session.get_credentials.return_value.access_key = 'abc123'
        bc_session.get_config_variable.return_value = 'us-west-2'

        session = Session('abc123', region_name='us-west-2')

        self.assertEqual(repr(session), 'Session(region_name=\'us-west-2\')')

    def test_repr_on_subclasses(self):
        bc_session = self.bc_session_cls.return_value
        bc_session.get_credentials.return_value.access_key = 'abc123'
        bc_session.get_config_variable.return_value = 'us-west-2'

        class MySession(Session):
            pass

        session = MySession('abc123', region_name='us-west-2')

        self.assertEqual(repr(session), 'MySession(region_name=\'us-west-2\')')

    def test_can_access_region_name(self):
        bc_session = self.bc_session_cls.return_value
        bc_session.get_config_variable.return_value = 'us-west-2'
        session = Session('abc123', region_name='us-west-2')
        bc_session.set_config_variable.assert_called_with('region',
                                                          'us-west-2')

        self.assertEqual(session.region_name, 'us-west-2')

    def test_arguments_not_required(self):
        Session()

        self.assertTrue(self.bc_session_cls.called,
                        'Botocore session was not created')

    def test_credentials_can_be_set(self):
        bc_session = self.bc_session_cls.return_value

        # Set values in constructor
        Session(aws_access_key_id='key',
                aws_secret_access_key='secret',
                aws_session_token='token')

        self.assertTrue(self.bc_session_cls.called,
                        'Botocore session was not created')
        self.assertTrue(bc_session.set_credentials.called,
                        'Botocore session set_credentials not called from constructor')
        bc_session.set_credentials.assert_called_with(
            access_key='key', secret_key='secret', token='token', auth_function=None, 
            token_manager=None, ibm_api_key_id=None, ibm_auth_endpoint=None, ibm_service_instance_id=None)

    def test_can_get_credentials(self):
        access_key = 'foo'
        secret_key = 'bar'
        token = 'baz'

        creds = mock.Mock()
        creds.access_key = access_key
        creds.secret_key = secret_key
        creds.token = token

        bc_session = self.bc_session_cls.return_value
        bc_session.get_credentials.return_value = creds

        session = Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=token)

        credentials = session.get_credentials()
        self.assertEqual(credentials.access_key, access_key)
        self.assertEqual(credentials.secret_key, secret_key)
        self.assertEqual(credentials.token, token)

    def test_profile_can_be_set(self):
        bc_session = self.bc_session_cls.return_value

        session = Session(profile_name='foo')

        bc_session.set_config_variable.assert_called_with(
            'profile', 'foo')
        bc_session.profile = 'foo'

        # We should also be able to read the value
        self.assertEqual(session.profile_name, 'foo')

    def test_profile_default(self):
        self.bc_session_cls.return_value.profile = None

        session = Session()

        self.assertEqual(session.profile_name, 'default')

    def test_available_profiles(self):
        bc_session = mock.Mock()
        bc_session.available_profiles.return_value = ['foo','bar']
        session = Session(botocore_session=bc_session)
        profiles = session.available_profiles
        self.assertEqual(len(profiles.return_value), 2)

    def test_custom_session(self):
        bc_session = self.bc_session_cls()
        self.bc_session_cls.reset_mock()

        Session(botocore_session=bc_session)

        # No new session was created
        self.assertFalse(self.bc_session_cls.called)

    def test_user_agent(self):
        # Here we get the underlying Botocore session, create a Boto 3
        # session, and ensure that the user-agent is modified as expected
        bc_session = self.bc_session_cls.return_value
        bc_session.user_agent_name = 'ibm-cos-sdk-python-core'
        bc_session.user_agent_version = '0.68.0'
        bc_session.user_agent_extra = ''

        Session(botocore_session=bc_session)

        self.assertEqual(bc_session.user_agent_name, 'ibm-cos-sdk-python')
        self.assertEqual(bc_session.user_agent_version, __version__)
        self.assertEqual(bc_session.user_agent_extra, 'ibm-cos-sdk-python-core/0.68.0')

    def test_user_agent_extra(self):
        # This test is the same as above, but includes custom extra content
        # which must still be in the final modified user-agent.
        bc_session = self.bc_session_cls.return_value
        bc_session.user_agent_name = 'ibm-cos-sdk-python-core'
        bc_session.user_agent_version = '0.68.0'
        bc_session.user_agent_extra = 'foo'

        Session(botocore_session=bc_session)

        self.assertEqual(bc_session.user_agent_extra, 'foo ibm-cos-sdk-python-core/0.68.0')

    def test_custom_user_agent(self):
        # This test ensures that a customized user-agent is left untouched.
        bc_session = self.bc_session_cls.return_value
        bc_session.user_agent_name = 'Custom'
        bc_session.user_agent_version = '1.0'
        bc_session.user_agent_extra = ''

        Session(botocore_session=bc_session)

        self.assertEqual(bc_session.user_agent_name, 'Custom')
        self.assertEqual(bc_session.user_agent_version, '1.0')
        self.assertEqual(bc_session.user_agent_extra, '')

    def test_get_available_services(self):
        bc_session = self.bc_session_cls.return_value

        session = Session()
        session.get_available_services()

        self.assertTrue(bc_session.get_available_services.called,
                        'Botocore session get_available_services not called')

    def test_get_available_resources(self):
        mock_bc_session = mock.Mock()
        loader = mock.Mock(spec=loaders.Loader)
        loader.list_available_services.return_value = ['foo', 'bar']
        mock_bc_session.get_component.return_value = loader
        session = Session(botocore_session=mock_bc_session)

        names = session.get_available_resources()
        self.assertEqual(names, ['foo', 'bar'])

    def test_get_available_partitions(self):
        bc_session = mock.Mock()
        bc_session.get_available_partitions.return_value = ['foo']
        session = Session(botocore_session=bc_session)

        partitions = session.get_available_partitions()
        self.assertEqual(partitions, ['foo'])

    def test_get_available_regions(self):
        bc_session = mock.Mock()
        bc_session.get_available_regions.return_value = ['foo']
        session = Session(botocore_session=bc_session)

        partitions = session.get_available_regions('myservice')
        bc_session.get_available_regions.assert_called_with(
            service_name='myservice', partition_name='aws',
            allow_non_regional=False
        )
        self.assertEqual(partitions, ['foo'])

    def test_create_client(self):
        session = Session(region_name='us-east-1')
        client = session.client('s3', region_name='us-west-2')

        self.assertTrue(client,
                        'No low-level client was returned')

    def test_create_client_with_args(self):
        bc_session = self.bc_session_cls.return_value

        session = Session(region_name='us-east-1')
        session.client('s3', region_name='us-west-2')

        bc_session.create_client.assert_called_with(
            's3', aws_secret_access_key=None, aws_access_key_id=None,
            endpoint_url=None, use_ssl=True, aws_session_token=None,
            verify=None, region_name='us-west-2', api_version=None,
            config=None, ibm_api_key_id=None, ibm_service_instance_id=None,
            ibm_auth_endpoint=None, auth_function=None, token_manager=None)

    def test_create_resource_with_args(self):
        mock_bc_session = mock.Mock()
        loader = mock.Mock(spec=loaders.Loader)
        loader.determine_latest_version.return_value = '2014-11-02'
        loader.load_service_model.return_value = {
            'resources': [], 'service': []}
        mock_bc_session.get_component.return_value = loader
        session = Session(botocore_session=mock_bc_session)
        session.resource_factory.load_from_definition = mock.Mock()
        session.client = mock.Mock()

        session.resource('s3', verify=False)

        session.client.assert_called_with(
            's3', aws_secret_access_key=None, aws_access_key_id=None,
            endpoint_url=None, use_ssl=True, aws_session_token=None,
            verify=False, region_name=None, api_version='2014-11-02',
            config=mock.ANY, auth_function=None, token_manager=None,
            ibm_api_key_id=None, ibm_auth_endpoint=None, ibm_service_instance_id=None)
        client_config = session.client.call_args[1]['config']
        self.assertEqual(client_config.user_agent_extra, 'Resource')
        self.assertEqual(client_config.signature_version, None)

    def test_create_resource_with_config(self):
        mock_bc_session = mock.Mock()
        loader = mock.Mock(spec=loaders.Loader)
        loader.determine_latest_version.return_value = '2014-11-02'
        loader.load_service_model.return_value = {
            'resources': [], 'service': []}
        mock_bc_session.get_component.return_value = loader
        session = Session(botocore_session=mock_bc_session)
        session.resource_factory.load_from_definition = mock.Mock()
        session.client = mock.Mock()
        config = Config(signature_version='v4')

        session.resource('s3', config=config)

        session.client.assert_called_with(
            's3', aws_secret_access_key=None, aws_access_key_id=None,
            endpoint_url=None, use_ssl=True, aws_session_token=None,
            verify=None, region_name=None, api_version='2014-11-02',
            config=mock.ANY, auth_function=None, token_manager=None,
            ibm_api_key_id=None, ibm_auth_endpoint=None, ibm_service_instance_id=None)
        client_config = session.client.call_args[1]['config']
        self.assertEqual(client_config.user_agent_extra, 'Resource')
        self.assertEqual(client_config.signature_version, 'v4')

    def test_create_resource_with_config_override_user_agent_extra(self):
        mock_bc_session = mock.Mock()
        loader = mock.Mock(spec=loaders.Loader)
        loader.determine_latest_version.return_value = '2014-11-02'
        loader.load_service_model.return_value = {
            'resources': [], 'service': []}
        mock_bc_session.get_component.return_value = loader
        session = Session(botocore_session=mock_bc_session)
        session.resource_factory.load_from_definition = mock.Mock()
        session.client = mock.Mock()
        config = Config(signature_version='v4', user_agent_extra='foo')

        session.resource('s3', config=config)

        session.client.assert_called_with(
            's3', aws_secret_access_key=None, aws_access_key_id=None,
            endpoint_url=None, use_ssl=True, aws_session_token=None,
            verify=None, region_name=None, api_version='2014-11-02',
            config=mock.ANY, auth_function=None, token_manager=None,
            ibm_api_key_id=None, ibm_auth_endpoint=None, ibm_service_instance_id=None)
        client_config = session.client.call_args[1]['config']
        self.assertEqual(client_config.user_agent_extra, 'foo')
        self.assertEqual(client_config.signature_version, 'v4')

    def test_create_resource_latest_version(self):
        mock_bc_session = mock.Mock()
        loader = mock.Mock(spec=loaders.Loader)
        loader.determine_latest_version.return_value = '2014-11-02'
        loader.load_service_model.return_value = {
            'resources': [], 'service': []}
        mock_bc_session.get_component.return_value = loader
        session = Session(botocore_session=mock_bc_session)
        session.resource_factory.load_from_definition = mock.Mock()

        session.resource('s3')

        loader.load_service_model.assert_called_with(
            's3', 'resources-1', None)

    def test_bad_resource_name(self):
        mock_bc_session = mock.Mock()
        loader = mock.Mock(spec=loaders.Loader)
        loader.load_service_model.side_effect = UnknownServiceError(
            service_name='foo', known_service_names='asdf'
        )
        mock_bc_session.get_component.return_value = loader
        loader.list_available_services.return_value = ['good-resource']
        mock_bc_session.get_available_services.return_value = ['s3']

        session = Session(botocore_session=mock_bc_session)
        with self.assertRaises(ResourceNotExistsError) as e:
            session.resource('s3')
        err_msg = str(e.exception)
        # 1. should say the resource doesn't exist.
        self.assertIn('resource does not exist', err_msg)
        self.assertIn('s3', err_msg)
        # 2. Should list available resources you can choose.
        self.assertIn('good-resource', err_msg)
        # 3. Should list client if available.
        self.assertIn('client', err_msg)

    def test_bad_resource_name_with_no_client_has_simple_err_msg(self):
        mock_bc_session = mock.Mock()
        loader = mock.Mock(spec=loaders.Loader)
        loader.load_service_model.side_effect = UnknownServiceError(
            service_name='foo', known_service_names='asdf'
        )
        mock_bc_session.get_component.return_value = loader
        loader.list_available_services.return_value = ['good-resource']
        mock_bc_session.get_available_services.return_value = ['good-client']

        session = Session(botocore_session=mock_bc_session)
        with self.assertRaises(ResourceNotExistsError) as e:
            session.resource('bad-client')
        err_msg = str(e.exception)
        # Shouldn't mention anything about clients because
        # 'bad-client' it not a valid ibm_boto3.client(...)
        self.assertNotIn('ibm_boto3.client', err_msg)

    def test_can_reach_events(self):
        mock_bc_session = self.bc_session_cls()
        session = Session(botocore_session=mock_bc_session)
        session.events
        mock_bc_session.get_component.assert_called_with('event_emitter')
