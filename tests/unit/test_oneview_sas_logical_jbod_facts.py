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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasLogicalJbodFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Sas-logical-Jbod",
    options=[]
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/sas-logical-jbods/c6bf9af9-48e7-4236-b08a-77684dc258a5",
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test-Sas-logical-Jbod",
    options=["jbod_drives"]
)

PRESENT_SAS_LOGICAL_JBODS = [{
    "name": "Test-Sas-logical-Jbod",
    "uri": "/rest/sas-logical-jbods/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]

SAS_JBOD_DRIVES = {
    "name": "Drive 39",
    "uri": "/rest/drive-enclosures/SN123102/drive-bays/29b-eadf8/drives/9156e9c"
}


@pytest.mark.resource(TestSasLogicalJbodFactsModule='sas_logical_jbods')
class TestSasLogicalJbodFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_sas_jbods(self):
        self.resource.get_all.return_value = PRESENT_SAS_LOGICAL_JBODS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=(PRESENT_SAS_LOGICAL_JBODS))
        )

    def test_get_sas_jbod_by_name_without_matching_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=[])
        )

    def test_should_get_sas_jbod_by_name(self):
        self.resource.data = PRESENT_SAS_LOGICAL_JBODS[0]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=(PRESENT_SAS_LOGICAL_JBODS))

        )

    def test_should_get_sas_jbod_by_uri(self):
        self.resource.data = PRESENT_SAS_LOGICAL_JBODS[0]
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=(PRESENT_SAS_LOGICAL_JBODS))

        )

    def test_should_get_sas_jbod_by_name_with_options(self):
        self.resource.data = PRESENT_SAS_LOGICAL_JBODS[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.resource.get_by.return_value = PRESENT_SAS_LOGICAL_JBODS

        self.resource.get_drives.return_value = SAS_JBOD_DRIVES

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        SasLogicalJbodFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbods=PRESENT_SAS_LOGICAL_JBODS,
                               jbod_drives=SAS_JBOD_DRIVES)
        )


if __name__ == '__main__':
    pytest.main([__file__])
