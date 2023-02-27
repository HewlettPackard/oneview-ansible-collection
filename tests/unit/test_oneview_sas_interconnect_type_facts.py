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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasInterconnectTypeFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Sas-interconnect-type-1",
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/sas-interconnect-types/c6bf9af9-58a5",
)

PRESENT_SAS_INTERCONNECT_TYPES = [{
    "name": "Test-Sas-interconnect-type-1",
    "uri": "/rest/sas-interconnect-types/c6bf9af9-58a5"
}]


@pytest.mark.resource(TestSasInterconnectTypeFactsModule='sas_interconnect_types')
class TestSasInterconnectTypeFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_sas_interconnect_types(self):
        self.resource.get_by_name.return_value = None
        self.resource.get_all.return_value = PRESENT_SAS_INTERCONNECT_TYPES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasInterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect_types=(PRESENT_SAS_INTERCONNECT_TYPES))
        )

    def test_get_sas_interconnect_type_by_name_without_matching_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasInterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect_types=[])
        )

    def test_should_get_sas_interconnect_type_by_name(self):
        self.resource.data = PRESENT_SAS_INTERCONNECT_TYPES[0]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasInterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect_types=(PRESENT_SAS_INTERCONNECT_TYPES))

        )

    def test_should_get_sas_interconnect_type_by_uri(self):
        self.resource.data = PRESENT_SAS_INTERCONNECT_TYPES[0]
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        SasInterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnect_types=(PRESENT_SAS_INTERCONNECT_TYPES))
        )


if __name__ == '__main__':
    pytest.main([__file__])
