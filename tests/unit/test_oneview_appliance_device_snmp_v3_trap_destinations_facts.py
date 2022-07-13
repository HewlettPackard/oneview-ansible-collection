#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ApplianceDeviceSnmpV3TrapDestinationsFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json'
)

PARAMS_GET_ALL = dict(
    config='config.json'
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name='1.1.1.1'
)

PRESENT_CONFIGURATION = {
    "category": "SnmpV3Destination",
    "destinationAddress": "1.1.1.1",
    "id": "abe0c97f-e8fc-4083-8dad-d22742b1c2af",
    "port": 162,
    "trapType": "TRAP",
    "type": "Destination",
    "uri": "/rest/appliance/snmpv3-trap-forwarding/destinations/abe0c97f-e8fc-4083-8dad-d22742b1c2af",
    "userId": "3953867c-5283-4059-a9ae-33487f901e85",
    "userUri": "/rest/appliance/snmpv3-trap-forwarding/users/3953867c-5283-4059-a9ae-33487f901e85"
}


@pytest.mark.resource(TestApplianceDeviceSnmpV3TrapDestinationsFactsModule='appliance_device_snmp_v3_trap_destinations')
class TestApplianceDeviceSnmpV3TrapDestinationsFactsModule(OneViewBaseFactsTest):
    @pytest.fixture(autouse=True)
    def specific_set_up(self, setUp):
        self.mock_ov_client.api_version = 600

    def test_should_get_all_snmp_v3_trap_destinations(self):
        ALL_TRAPS = [PRESENT_CONFIGURATION]
        self.resource.get_all.return_value = ALL_TRAPS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ApplianceDeviceSnmpV3TrapDestinationsFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_device_snmp_v3_trap_destinations=ALL_TRAPS)
        )

    def test_should_get_by_id_snmp_v3_trap_destinations(self):
        self.resource.data = PRESENT_CONFIGURATION
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ApplianceDeviceSnmpV3TrapDestinationsFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_device_snmp_v3_trap_destinations=PRESENT_CONFIGURATION)
        )


if __name__ == '__main__':
    pytest.main([__file__])
