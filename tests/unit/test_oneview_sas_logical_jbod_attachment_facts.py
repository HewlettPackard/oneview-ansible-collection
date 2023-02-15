#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2023) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasLogicalJbodAttachmentFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Sas-logical-Jbod-Attachment",
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/sas-logical-jbod-attachments/c6bf9af9-58a5",
)

PRESENT_SAS_LOGICAL_JBOD_ATTACHMENTS = [{
    "name": "Test-Sas-logical-Jbod-Attachment",
    "uri": "/rest/sas-logical-jbod-attachments/c6bf9c258a5"
}]


@pytest.mark.resource(TestSasLogicalJbodAttachmentFactsModule='sas_logical_jbod_attachments')
class TestSasLogicalJbodAttachmentFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_sas_jbod_attachments(self):
        self.resource.get_by_name.return_value = None
        self.resource.get_all.return_value = PRESENT_SAS_LOGICAL_JBOD_ATTACHMENTS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasLogicalJbodAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbod_attachments=(PRESENT_SAS_LOGICAL_JBOD_ATTACHMENTS))
        )

    def test_get_sas_jbod_attachment_by_name_without_matching_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalJbodAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbod_attachments=[])
        )

    def test_should_get_sas_jbod_attachment_by_name(self):
        self.resource.data = PRESENT_SAS_LOGICAL_JBOD_ATTACHMENTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalJbodAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbod_attachments=(PRESENT_SAS_LOGICAL_JBOD_ATTACHMENTS))

        )

    def test_should_get_sas_jbod_by_uri(self):
        self.resource.data = PRESENT_SAS_LOGICAL_JBOD_ATTACHMENTS[0]
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        SasLogicalJbodAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbod_attachments=(PRESENT_SAS_LOGICAL_JBOD_ATTACHMENTS))
        )


if __name__ == '__main__':
    pytest.main([__file__])
