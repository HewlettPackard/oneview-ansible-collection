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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasLogicalInterconnectFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Sas-logical-Interconnect",
    options=[]
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/sas-logical-interconnects/c6bf9af9-48e7-4236-b08a-77684dc258a5",
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test-Sas-logical-Interconnect",
    options=["firmware_facts"]
)

PRESENT_SAS_LOGICAL_INTERCONNECTS = [{
    "name": "Test-Sas-logical-Inetrconnect",
    "uri": "/rest/sas-logical-interconnects/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]

SAS_LI_FIRMWARE_FACTS = {
    "interconnects": [{
        "interconnectUri": "/rest/sas-interconnects/2M220105SL",
        "model": "Synergy 12Gb SAS Connection Module",
        "installedFw": "1.5.203.0"
    }]
}


@pytest.mark.resource(TestSasLogicalInterconnectFactsModule='sas_logical_interconnects')
class TestSasLogicalInterconnectFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_sas_logical_interconnects(self):
        self.resource.get_by_name.return_value = None
        self.resource.get_all.return_value = PRESENT_SAS_LOGICAL_INTERCONNECTS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasLogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnects=(PRESENT_SAS_LOGICAL_INTERCONNECTS))
        )

    def test_get_sas_li_by_name_without_matching_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnects=[])
        )

    def test_should_get_sas_li_by_name(self):
        self.resource.data = PRESENT_SAS_LOGICAL_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnects=(PRESENT_SAS_LOGICAL_INTERCONNECTS))

        )

    def test_should_get_sas_li_by_uri(self):
        self.resource.data = PRESENT_SAS_LOGICAL_INTERCONNECTS[0]
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        SasLogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnects=(PRESENT_SAS_LOGICAL_INTERCONNECTS))

        )

    def test_should_get_sas_li_by_name_with_options(self):
        self.resource.data = PRESENT_SAS_LOGICAL_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.resource.get_by.return_value = PRESENT_SAS_LOGICAL_INTERCONNECTS[0]

        self.resource.get_firmware.return_value = SAS_LI_FIRMWARE_FACTS

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        SasLogicalInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnects=PRESENT_SAS_LOGICAL_INTERCONNECTS,
                               firmware_facts=SAS_LI_FIRMWARE_FACTS)
        )


if __name__ == '__main__':
    pytest.main([__file__])
