#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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

import mock
import pytest

from copy import deepcopy
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ApplianceNetworkInterfacesModule

ERROR_MSG = 'Fake message error'

DEFAULT_PARAMS = {
    "macAddress": "00:00:11:28:j8:90",
    "ipv4Type": "STATIC",
    "ipv6Type": "UNCONFIGURE",
    "hostname": "ci-00505698f13e.com",
    "app1Ipv4Addr": "1.1.1.1",
    "app2Ipv4Addr": "1.1.1.2",
    "virtIpv4Addr": "1.1.1.3",
    "ipv4Subnet": "255.255.0.0",
    "ipv4Gateway": "10.10.1.1",
    "ipv4NameServers": [
        "16.17.18.19",
        "16.17.18.20"
    ]
}

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=DEFAULT_PARAMS,
)


@pytest.mark.resource(TestApplianceNetworkInterfacesModule='appliance_network_interfaces')
class TestApplianceNetworkInterfacesModule(OneViewBaseTest):
    def test_should_create_network_interface(self):
        self.resource.get_by_mac_address.return_value = None
        self.resource.data = DEFAULT_PARAMS
        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceNetworkInterfacesModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceNetworkInterfacesModule.MSG_CREATED,
            ansible_facts=dict(appliance_network_interfaces=DEFAULT_PARAMS)
        )

    def test_should_do_nothing_when_network_interface_exist(self):
        self.resource.data = DEFAULT_PARAMS

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceNetworkInterfacesModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceNetworkInterfacesModule.MSG_ALREADY_PRESENT
        )

    def test_should_update_when_network_interface_has_different_attributes(self):
        network_data = deepcopy(DEFAULT_PARAMS)
        network_data['ipv4NameServers'] = ['16.17.18.21', '16.17.18.22']

        self.resource.get_by_mac_address.return_value = self.resource
        self.resource.data = deepcopy(DEFAULT_PARAMS)

        self.resource.create.return_value = network_data

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceNetworkInterfacesModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceNetworkInterfacesModule.MSG_CREATED,
            ansible_facts=dict(appliance_network_interfaces=network_data)
        )


if __name__ == '__main__':
    pytest.main([__file__])
