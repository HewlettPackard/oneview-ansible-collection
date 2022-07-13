#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
import yaml

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import InterconnectFactsModule

ERROR_MSG = 'Fake message error'

INTERCONNECT_NAME = "0000A66102, interconnect 2"

PARAMS_FOR_GET_ALL = dict(
    config='config.json',
    name=None,
)

PARAMS_FOR_GET_BY_NAME = dict(
    config='config.json',
    name=INTERCONNECT_NAME
)

PARAMS_FOR_GET_NAME_SERVERS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=['nameServers']
)

INTERCONNECT_URI = "/rest/interconnects/53fa7d35-1cc8-46c1-abf0-6af091a1aed3"
INTERCONNECT_ID = "53fa7d35-1cc8-46c1-abf0-6af091a1aed3"
PORT_NAME = "d1"
SUBPORT_NUMBER = 1

PARAMS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=['statistics']
)

PARAMS_PLUGGABLE_MODULE = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=['pluggableModuleInformation']
)

PARAMS_FOR_PORT_STATISTICS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=[{'portStatistics': PORT_NAME}]
)

PARAMS_FOR_SUBPORT_STATISTICS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=[{'subPortStatistics': {'portName': PORT_NAME, 'subportNumber': SUBPORT_NUMBER}}]
)

PARAMS_FOR_GET_PORT = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=[{'port': 'd1'}]
)

PARAMS_FOR_GET_PORTS = dict(
    config='config.json',
    name=INTERCONNECT_NAME,
    options=['ports']
)


MOCK_INTERCONNECTS = [
    dict(uidState='On', uri=INTERCONNECT_URI)
]

MOCK_INTERCONNECTS_ID = [
    dict(uidState='On', uri=INTERCONNECT_ID)
]


@pytest.mark.resource(TestInterconnectFactsModule='interconnects')
class TestInterconnectFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_interconnects(self):
        fake_interconnects = [dict(uidState='On', name=INTERCONNECT_NAME)]
        self.resource.get_all.return_value = fake_interconnects

        self.mock_ansible_module.params = PARAMS_FOR_GET_ALL

        InterconnectFactsModule().run()

        self.resource.get_all.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=fake_interconnects)
        )

    def test_should_get_interconnects_by_interconnect_name(self):
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_GET_BY_NAME

        InterconnectFactsModule().run()

        self.resource.get_by_name.assert_called_once_with(INTERCONNECT_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS)
        )

    def test_should_get_interconnect_name_servers(self):
        fake_name_servers = [dict(t=1)]
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_name_servers.return_value = fake_name_servers

        self.mock_ansible_module.params = PARAMS_FOR_GET_NAME_SERVERS

        InterconnectFactsModule().run()

        self.resource.get_by_name.assert_called_once_with(INTERCONNECT_NAME)
        self.resource.get_name_servers.assert_called_once()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS, interconnect_name_servers=fake_name_servers)
        )

    def test_should_get_interconnect_statistics_by_interconnect_name(self):
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource

        fake_statistics = dict()
        self.resource.get_statistics.return_value = fake_statistics

        self.mock_ansible_module.params = PARAMS

        InterconnectFactsModule().run()

        self.resource.get_statistics.assert_called_once()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                interconnects=MOCK_INTERCONNECTS,
                interconnect_statistics=fake_statistics,

            )
        )

    def test_should_gather_facts_about_interconnect_port_statistics(self):
        fake_statistics = dict(name='test')
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_statistics.return_value = fake_statistics

        self.mock_ansible_module.params = PARAMS_FOR_PORT_STATISTICS

        InterconnectFactsModule().run()

        self.resource.get_statistics.assert_called_once_with(PORT_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                interconnects=MOCK_INTERCONNECTS,
                interconnect_port_statistics=fake_statistics,
            )
        )

    def test_should_gather_facts_about_interconnect_subport_statistics(self):
        fake_statistics = dict(name='test')
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_subport_statistics.return_value = fake_statistics

        self.mock_ansible_module.params = PARAMS_FOR_SUBPORT_STATISTICS

        InterconnectFactsModule().run()

        self.resource.get_subport_statistics.assert_called_once_with(
            PORT_NAME,
            SUBPORT_NUMBER
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                interconnects=MOCK_INTERCONNECTS,
                interconnect_subport_statistics=fake_statistics
            )
        )

    def test_should_get_interconnect_ports(self, testing_module):
        fake_ports = [dict(t=1), dict(t=2)]
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_ports.return_value = fake_ports

        self.mock_ansible_module.params = PARAMS_FOR_GET_PORTS

        InterconnectFactsModule().run()

        self.resource.get_by_name.assert_called_once_with(INTERCONNECT_NAME)
        self.resource.get_ports.assert_called_once()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS, interconnect_ports=fake_ports)
        )

    def test_should_get_interconnect_port(self, testing_module):
        fake_port = dict(t=1)
        port_id = "53fa7d35-1cc8-46c1-abf0-6af091a1aed3:d1"
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource

        self.resource.get_by_name.return_value = self.resource
        self.resource.get_port.return_value = fake_port

        self.mock_ansible_module.params = PARAMS_FOR_GET_PORT

        InterconnectFactsModule().run()

        self.resource.get_by_name.assert_called_once_with(INTERCONNECT_NAME)
        self.resource.get_port.assert_called_once_with(port_id)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS, interconnect_port=fake_port)
        )

    def test_should_get_interconnect_port_using_id(self, testing_module):
        fake_port = dict(t=1)
        port_id = "53fa7d35-1cc8-46c1-abf0-6af091a1aed3:d1"
        self.resource.data = MOCK_INTERCONNECTS_ID[0]
        self.resource.get_by_name.return_value = self.resource

        self.resource.get_by_name.return_value = self.resource
        self.resource.get_port.return_value = fake_port

        self.mock_ansible_module.params = PARAMS_FOR_GET_PORT

        InterconnectFactsModule().run()

        self.resource.get_by_name.assert_called_once_with(INTERCONNECT_NAME)
        self.resource.get_port.assert_called_once_with(port_id)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS_ID, interconnect_port=fake_port)
        )

    def test_should_get_pluggable_module_information(self):
        fake_sfp_info = [dict(t=1), dict(t=2)]
        self.resource.data = MOCK_INTERCONNECTS[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_pluggable_module_information.return_value = fake_sfp_info

        self.mock_ansible_module.params = PARAMS_PLUGGABLE_MODULE

        InterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnects=MOCK_INTERCONNECTS,
                               interconnect_pluggable_module_information=fake_sfp_info)
        )


if __name__ == '__main__':
    pytest.main([__file__])
