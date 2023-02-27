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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasLogicalInterconnectGroupFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Sas-logical-interconnect-groups"
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/sas-logical-interconnect-groups/c6bf9af9-58a5",
)

SAS_LOGICAL_INTERCONNECT_GROUP_FROM_ONEVIEW = [{
    "name": "Test-Sas-logical-interconnect-groups",
    "uri": "/rest/sas-logical-interconnect-groups/c6bf9af9-58a5"
}]


@pytest.mark.resource(TestSasLogicalInterconnectGroupFactsModule='sas_logical_interconnect_groups')
class TestSasLogicalInterconnectGroupFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_sas_logical_interconnect_groups(self):
        self.resource.get_by_name.return_value = None
        self.resource.get_all.return_value = SAS_LOGICAL_INTERCONNECT_GROUP_FROM_ONEVIEW
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasLogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnect_groups=(SAS_LOGICAL_INTERCONNECT_GROUP_FROM_ONEVIEW))
        )

    def test_get_sas_lig_by_name_without_matching_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnect_groups=[])
        )

    def test_should_get_sas_lig_by_name(self):
        self.resource.data = SAS_LOGICAL_INTERCONNECT_GROUP_FROM_ONEVIEW[0]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasLogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnect_groups=(SAS_LOGICAL_INTERCONNECT_GROUP_FROM_ONEVIEW))

        )

    def test_should_get_sas_interconnect_by_uri(self):
        self.resource.data = SAS_LOGICAL_INTERCONNECT_GROUP_FROM_ONEVIEW[0]
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        SasLogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnect_groups=(SAS_LOGICAL_INTERCONNECT_GROUP_FROM_ONEVIEW))
        )


if __name__ == '__main__':
    pytest.main([__file__])
