# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# https://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import random
import time
import unittest
from unittest import mock


def unique_id(name):
    """
    Generate a unique ID that includes the given name,
    a timestamp and a random number. This helps when running
    integration tests in parallel that must create remote
    resources.
    """
    return f'{name}-{int(time.time())}-{random.randint(0, 10000)}'


class BaseTestCase(unittest.TestCase):
    """
    A base test case which mocks out the low-level session to prevent
    any actual calls to Botocore.
    """

    def setUp(self):
        self.bc_session_patch = mock.patch('ibm_botocore.session.Session')
        self.bc_session_cls = self.bc_session_patch.start()

        loader = self.bc_session_cls.return_value.get_component.return_value
        loader.data_path = ''
        self.loader = loader

        # We also need to patch the global default session.
        # Otherwise it could be a cached real session came from previous
        # "functional" or "integration" tests.
        patch_global_session = mock.patch('ibm_boto3.DEFAULT_SESSION')
        patch_global_session.start()
        self.addCleanup(patch_global_session.stop)

    def tearDown(self):
        self.bc_session_patch.stop()
