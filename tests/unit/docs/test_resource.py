# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from ibm_boto3.docs.resource import ResourceDocumenter, ServiceResourceDocumenter
from tests.unit.docs import BaseDocsTest


class TestResourceDocumenter(BaseDocsTest):
    def test_document_resource(self):
        resource = self.resource.Sample('mysample')
        resource_documenter = ResourceDocumenter(
            resource, self.ibm_botocore_session, self.root_services_path
        )
        resource_documenter.document_resource(self.doc_structure)
        self.assert_contains_lines_in_order(
            [
                '======',
                'Sample',
                '======',
                'Before using anything on this page, please refer to the resources ',
                ':doc:`user guide <../../../../guide/resources>` for the most recent ',
                'guidance on using resources.',
                '.. py:class:: MyService.Sample(name)',
                '  A resource representing an AWS MyService Sample::',
                '    import ibm_boto3',
                "    myservice = ibm_boto3.resource('myservice')",
                "    sample = myservice.Sample('name')",
                'Identifiers',
                "These are the resource's available identifiers:",
                '.. toctree::',
                '  :maxdepth: 1',
                '  :titlesonly:',
                '  name',
                'Attributes',
                "These are the resource's available attributes:",
                '.. toctree::',
                '  :maxdepth: 1',
                '  :titlesonly:',
                '  bar',
                '  foo',
                'Actions',
                "These are the resource's available actions:",
                '.. toctree::',
                '  :maxdepth: 1',
                '  :titlesonly:',
                '  load',
                '  operate',
                '  reload',
                'Waiters',
                "These are the resource's available waiters:",
                '.. toctree::',
                '  :maxdepth: 1',
                '  :titlesonly:',
                '  wait_until_complete',
            ]
        )
        self.assert_contains_lines_in_order(
            [
                'name',
                '.. py:attribute:: MyService.Sample.name',
            ],
            self.get_nested_service_contents('myservice', 'sample', 'name'),
        )
        self.assert_contains_lines_in_order(
            [
                'bar',
                '.. py:attribute:: MyService.Sample.bar',
                '  - *(string) --* Documents Bar',
            ],
            self.get_nested_service_contents('myservice', 'sample', 'bar'),
        )
        self.assert_contains_lines_in_order(
            [
                'load',
                '.. py:method:: MyService.Sample.load()',
            ],
            self.get_nested_service_contents('myservice', 'sample', 'load'),
        )
        self.assert_contains_lines_in_order(
            [
                'wait_until_complete',
                '.. py:method:: MyService.Sample.wait_until_complete(**kwargs)',
            ],
            self.get_nested_service_contents(
                'myservice', 'sample', 'wait_until_complete'
            ),
        )


class TestServiceResourceDocumenter(BaseDocsTest):
    def test_document_resource(self):
        resource_documenter = ServiceResourceDocumenter(
            self.resource, self.ibm_botocore_session, self.root_services_path
        )
        resource_documenter.document_resource(self.doc_structure)
        self.assert_contains_lines_in_order(
            [
                '================',
                'Service Resource',
                '================',
                'Before using anything on this page, please refer to the resources ',
                ':doc:`user guide <../../../../guide/resources>` for the most recent ',
                'guidance on using resources.',
                '.. py:class:: MyService.ServiceResource()',
                '  A resource representing AWS MyService::',
                '    import ibm_boto3',
                "    myservice = ibm_boto3.resource('myservice')",
                'Actions',
                "These are the resource's available actions:",
                '.. toctree::',
                '  :maxdepth: 1',
                '  :titlesonly:',
                '  sample_operation',
                'Sub-resources',
                "These are the resource's available sub-resources:",
                '.. toctree::',
                '  :maxdepth: 1',
                '  :titlesonly:',
                '  Sample',
                'Collections',
                "These are the resource's available collections:",
                '.. toctree::',
                '  :maxdepth: 1',
                '  :titlesonly:',
                '  samples',
            ]
        )
        self.assert_contains_lines_in_order(
            [
                'sample_operation',
                '.. py:method:: MyService.ServiceResource.sample_operation(**kwargs)',
            ],
            self.get_nested_service_contents(
                'myservice', 'service-resource', 'sample_operation'
            ),
        )
        self.assert_contains_lines_in_order(
            [
                'Sample',
                '.. py:method:: MyService.ServiceResource.Sample(name)',
            ],
            self.get_nested_service_contents(
                'myservice', 'service-resource', 'Sample'
            ),
        )
        self.assert_contains_lines_in_order(
            [
                'samples',
                '.. py:attribute:: MyService.ServiceResource.samples',
                '  .. py:method:: all()',
                '  .. py:method:: filter(**kwargs)',
                '  .. py:method:: limit(**kwargs)',
                '  .. py:method:: page_size(**kwargs)',
            ],
            self.get_nested_service_contents(
                'myservice', 'service-resource', 'samples'
            ),
        )
