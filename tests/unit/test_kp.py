# Copyright 2017 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
import types
import unittest
import mock
import inspect

from boto3 import client
from boto3 import utils
from botocore.config import Config
from botocore.exceptions import ParamValidationError

class FakeModule(object):
    @staticmethod
    def entry_point(**kwargs):
        return kwargs


class TestKeyProtect(unittest.TestCase):
    crn = 'crn:v1:bluemix:public:KMS:us-South:a/MYIBMKEY:0123456789ABCDEF:key:MYKEY'

    def _get_client(self):
        return client('s3', 
                      ibm_api_key_id='MYAPIKEYID', 
                      ibm_service_instance_id='MYAPIKEYID', 
                      ibm_auth_endpoint='IBMAUTHENDPOINT', 
                      endpoint_url='https://192.168.0.1:443',
                      config=Config(signature_version='oauth'))

    def test_key_protect_create_bucket_can_specify_both_new_arguments(self):
        client = self._get_client()
        try:
            # Will fail because of invalid ibm_auth_endpoint, but we will prove that IBMSSEKMS* can be specified
            client.create_bucket(Bucket='Doesntmatter', IBMSSEKMSEncryptionAlgorithm='AES256', IBMSSEKMSCustomerRootKeyCrn=self.crn)
        except Exception as ex:
            self.assertEqual(True, str(ex).startswith('Invalid URL'))

    def test_key_protect_create_bucket_can_specify_only_crn(self):
        client = self._get_client()
        try:
            # Will fail because of invalid ibm_auth_endpoint, but we will prove that only IBMSSEKMSEncryptionAlgorithm can be specified
            client.create_bucket(Bucket='Doesntmatter', IBMSSEKMSCustomerRootKeyCrn='ROOTKEYCRN')
        except Exception as ex:
            self.assertEqual(True, str(ex).startswith('Invalid URL'))
