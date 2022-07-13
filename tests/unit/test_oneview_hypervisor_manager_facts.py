#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import HypervisorManagerFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="172.18.13.11"
)

PRESENT_HYPERVISORS = [{
    "name": "172.18.13.11",
    "uri": "/rest/hypervisor-managers/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


@pytest.mark.resource(TestHypervisorManagerFactsModule='hypervisor_managers')
class TestHypervisorManagerFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_hypervisor_managers(self):
        self.resource.get_all.return_value = PRESENT_HYPERVISORS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        HypervisorManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(hypervisor_managers=PRESENT_HYPERVISORS)
        )

    def test_should_get_hypervisor_manager_by_name(self):
        self.resource.get_by.return_value = PRESENT_HYPERVISORS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        HypervisorManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(hypervisor_managers=PRESENT_HYPERVISORS)
        )


if __name__ == '__main__':
    pytest.main([__file__])
