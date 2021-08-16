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

import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ApplianceNetworkInterfaceFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

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

NETWORK_INTERFACE = dict(
    config='config.json',
    data=dict(applianceNetworks=[DEFAULT_PARAMS])
)

PARAMS_GET_BY_MAC = dict(
    config='config.json',
    mac_address="00:00:11:28:j8:90")

PARAMS_GET_ALL_MAC_ADDRESS = dict(
    config='config.json',
    options=['getAllMacAddress'])


@pytest.mark.resource(TestApplianceNetworkInterfaceFactsModule='appliance_network_interfaces')
class TestApplianceNetworkInterfaceFactsModule(OneViewBaseTest):
    def test_should_get_all_network_interfaces(self):
        self.resource.get_all.return_value = self.resource
        self.resource.data = NETWORK_INTERFACE
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ApplianceNetworkInterfaceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_network_interfaces=NETWORK_INTERFACE)
        )

    def test_should_get_network_interface_by_mac_address(self):
        self.resource.get_by_mac_address.return_value = self.resource
        self.resource.data = NETWORK_INTERFACE
        self.mock_ansible_module.params = PARAMS_GET_BY_MAC

        ApplianceNetworkInterfaceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_network_interfaces=NETWORK_INTERFACE)
        )

    def test_should_get_all_unconfigured_mac_address(self):
        mac_addresses = [DEFAULT_PARAMS]
        self.resource.get_all_mac_address.return_value = mac_addresses

        self.mock_ansible_module.params = PARAMS_GET_ALL_MAC_ADDRESS

        ApplianceNetworkInterfaceFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_network_interfaces=mac_addresses)
        )


if __name__ == '__main__':
    pytest.main([__file__])
