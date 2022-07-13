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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ApplianceDeviceSnmpV3UsersModule, OneViewModuleException

ERROR_MSG = 'Fake message error'

DEFAULT_PARAMS = dict(
    userName='testUser666',
    securityLevel='Authentication',
    authenticationProtocol='SHA256'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    name=DEFAULT_PARAMS['userName'],
    data=DEFAULT_PARAMS,
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    name=DEFAULT_PARAMS['userName'],
    data=dict(userName=DEFAULT_PARAMS['userName'],
              authenticationProtocol='SHA512'),
)

PARAMS_FOR_SET_PASSWORD = dict(
    config='config.json',
    state='present',
    name=DEFAULT_PARAMS['userName'],
    data=dict(userName=DEFAULT_PARAMS['userName'],
              authenticationPassphrase='NewPass1234')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    name=DEFAULT_PARAMS['userName'])


@pytest.mark.resource(TestApplianceDeviceSnmpV3UsersModule='appliance_device_snmp_v3_users')
class TestApplianceDeviceSnmpV3UsersModule(OneViewBaseTest):

    def test_should_raise_exception_when_api_is_lower_than_600(self):
        self.mock_ov_client.api_version = 400
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV3UsersModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY,
            msg=ApplianceDeviceSnmpV3UsersModule.MSG_API_VERSION_ERROR
        )

    @pytest.fixture(autouse=True)
    def specific_set_up(self, setUp):
        self.mock_ov_client.api_version = 600

    def test_should_create_new_snmp_v3_user(self):
        self.resource.get_by_name.return_value = None
        self.resource.data = DEFAULT_PARAMS
        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV3UsersModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV3UsersModule.MSG_CREATED,
            ansible_facts=dict(appliance_device_snmp_v3_users=DEFAULT_PARAMS)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_PARAMS
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceDeviceSnmpV3UsersModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV3UsersModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(appliance_device_snmp_v3_users=DEFAULT_PARAMS)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_PARAMS.copy()
        self.resource.data = DEFAULT_PARAMS
        self.resource.get_by_name.return_value = self.resource
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        ApplianceDeviceSnmpV3UsersModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV3UsersModule.MSG_UPDATED,
            ansible_facts=dict(appliance_device_snmp_v3_users=data_merged)
        )

    def test_should_remove_snmp_v3_user(self):
        self.resource.get_by.return_value = [DEFAULT_PARAMS]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV3UsersModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceDeviceSnmpV3UsersModule.MSG_DELETED
        )

    def test_should_do_nothing_when_snmp_v3_user_not_exist(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceDeviceSnmpV3UsersModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceDeviceSnmpV3UsersModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
