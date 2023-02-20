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

import mock
import pytest

from copy import deepcopy
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasInterconnectModule

SAS_INTERCONNECT_FROM_ONEVIEW = dict(
    name="Sas-Interconnect",
    uri="/rest/sas-interconnects/197f33a3",
    category="sas-interconnects",
    powerState="On",
    uidState="Off",
    softResetState="Normal",
    hardResetState="Normal"
)

PARAMS_FOR_POWER_OFF = dict(
    config='config.json',
    state='power_off',
    data=dict(name='Sas-Interconnect')
)

PARAMS_FOR_POWER_ON = dict(
    config='config.json',
    state='power_on',
    data=dict(name='Sas-Interconnect')
)

PARAMS_FOR_UIDSTATE_OFF = dict(
    config='config.json',
    state='uid_off',
    data=dict(name='Sas-Interconnect')
)

PARAMS_FOR_UIDSTATE_ON = dict(
    config='config.json',
    state='uid_on',
    data=dict(name='Sas-Interconnect')
)

PARAMS_FOR_SOFT_RESET = dict(
    config='config.json',
    state='soft_reset',
    data=dict(name='Sas-Interconnect')
)

PARAMS_FOR_HARD_RESET = dict(
    config='config.json',
    state='hard_reset',
    data=dict(name='Sas-Interconnect')
)

PARAMS_WITHOUT_NAME = dict(
    config='config.json',
    state='soft_reset',
    data=dict()
)

PARAMS_FOR_REFRESH = dict(
    config='config.json',
    state='refreshed',
    data=dict(name='Sas-Interconnect',  
              refreshState = 'RefreshPending'
    )
)

PARAMS_FOR_REFRESH_WITHOUT_NAME= dict(
    config='config.json',
    state='refreshed',
    data=dict(refreshState = 'RefreshPending'
    )
)

@pytest.mark.resource(TestSasInterconnectModule='sas_interconnects')
class TestSasInterconnectModule(OneViewBaseTest):
    def test_should_power_off_sas_interconnect(self):
        self.mock_ansible_module.params = PARAMS_FOR_POWER_OFF

        self.resource.data = SAS_INTERCONNECT_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        resource_after_power_off = dict(SAS_INTERCONNECT_FROM_ONEVIEW, powerState="Off")
        self.resource.patch.return_value.data = resource_after_power_off

        SasInterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/powerState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_POWERED_OFF,
            ansible_facts=dict(sas_interconnects=resource_after_power_off)
        )

    def test_should_not_power_off_when_already_off(self):
        self.mock_ansible_module.params = PARAMS_FOR_POWER_OFF

        self.resource.data = dict(SAS_INTERCONNECT_FROM_ONEVIEW, powerState="Off")
        self.resource.get_by_name.return_value = self.resource

        SasInterconnectModule().run()

        self.resource.patch.had_not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_ALREADY_POWERED_OFF,
            ansible_facts=dict(sas_interconnects=self.resource.data)
        )

    def test_should_power_on_sas_interconnect(self):
        self.mock_ansible_module.params = PARAMS_FOR_POWER_ON

        self.resource.data = dict(SAS_INTERCONNECT_FROM_ONEVIEW, powerState="Off")
        self.resource.get_by_name.return_value = self.resource

        self.resource.patch.return_value.data = SAS_INTERCONNECT_FROM_ONEVIEW

        SasInterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/powerState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_POWERED_ON,
            ansible_facts=dict(sas_interconnects=SAS_INTERCONNECT_FROM_ONEVIEW)
        )

    def test_should_not_power_on_when_already_on(self):
        self.mock_ansible_module.params = PARAMS_FOR_POWER_ON

        self.resource.data = SAS_INTERCONNECT_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        SasInterconnectModule().run()

        self.resource.patch.had_not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_ALREADY_POWERED_ON,
            ansible_facts=dict(sas_interconnects=self.resource.data)
        )

    def test_should_set_uidstate_off(self):
        self.mock_ansible_module.params = PARAMS_FOR_UIDSTATE_OFF

        self.resource.data = dict(SAS_INTERCONNECT_FROM_ONEVIEW, uidState="On")
        self.resource.get_by_name.return_value = self.resource

        self.resource.patch.return_value.data = SAS_INTERCONNECT_FROM_ONEVIEW

        SasInterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/uidState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasInterconnectModule.MSG_UID_POWERED_OFF,
            ansible_facts=dict(sas_interconnects=SAS_INTERCONNECT_FROM_ONEVIEW)
        )

    def test_should_not_set_uid_off_when_already_off(self):
        self.mock_ansible_module.params = PARAMS_FOR_UIDSTATE_OFF

        self.resource.data = SAS_INTERCONNECT_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        SasInterconnectModule().run()

        self.resource.patch.had_not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_UID_ALREADY_POWERED_OFF,
            ansible_facts=dict(sas_interconnects=self.resource.data)
        )

    def test_should_set_uid_on(self):
        self.mock_ansible_module.params = PARAMS_FOR_UIDSTATE_ON

        self.resource.data = SAS_INTERCONNECT_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        resource_after_uid_on = dict(SAS_INTERCONNECT_FROM_ONEVIEW, uidState="On")
        self.resource.patch.return_value.data = resource_after_uid_on

        SasInterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/uidState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasInterconnectModule.MSG_UID_POWERED_ON,
            ansible_facts=dict(sas_interconnects=resource_after_uid_on)
        )

    def test_should_not_power_on_when_already_on(self):
        self.mock_ansible_module.params = PARAMS_FOR_UIDSTATE_ON

        self.resource.data = dict(SAS_INTERCONNECT_FROM_ONEVIEW, uidState="On")
        self.resource.get_by_name.return_value = self.resource

        SasInterconnectModule().run()

        self.resource.patch.had_not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_UID_ALREADY_POWERED_ON,
            ansible_facts=dict(sas_interconnects=self.resource.data)
        )

    def test_should_soft_reset_sas_interconnect(self):
        self.mock_ansible_module.params = PARAMS_FOR_SOFT_RESET

        self.resource.data = SAS_INTERCONNECT_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        self.resource.patch.return_value.data = SAS_INTERCONNECT_FROM_ONEVIEW

        SasInterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/softResetState',
            value='Reset'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasInterconnectModule.MSG_SOFT_RESET_SAS_INTERCONNECT,
            ansible_facts=dict(sas_interconnects=SAS_INTERCONNECT_FROM_ONEVIEW)
        )

    def test_should_fail_when_interconnect_not_found(self):
        self.mock_ansible_module.params = PARAMS_FOR_SOFT_RESET

        self.resource.get_by_uri.return_value = []
        self.resource.get_by_name.return_value = []

        SasInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_NOT_FOUND)

    def test_should_fail_when_interconnect_name_not_found(self):
        self.mock_ansible_module.params = PARAMS_WITHOUT_NAME

        self.resource.get_by_uri.return_value = []
        self.resource.get_by_name.return_value = []

        SasInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_NAME_REQUIRED)

    def test_should_hard_reset_sas_interconnect(self):
        self.mock_ansible_module.params = PARAMS_FOR_HARD_RESET

        self.resource.data = SAS_INTERCONNECT_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        self.resource.patch.return_value.data = SAS_INTERCONNECT_FROM_ONEVIEW

        SasInterconnectModule().run()

        self.resource.patch.assert_called_with(
            operation='replace',
            path='/hardResetState',
            value='Reset'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasInterconnectModule.MSG_HARD_RESET_SAS_INTERCONNECT,
            ansible_facts=dict(sas_interconnects=SAS_INTERCONNECT_FROM_ONEVIEW)
        )

    def test_should_refresh_sas_interconnect(self):
        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        self.resource.data = SAS_INTERCONNECT_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        self.resource.refresh_state.return_value.data = SAS_INTERCONNECT_FROM_ONEVIEW

        SasInterconnectModule().run()

        self.resource.refresh_state.assert_called_with({
            "refreshState": "RefreshPending"
        }
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_REFRESHED,
            ansible_facts=dict(sas_interconnects=SAS_INTERCONNECT_FROM_ONEVIEW)
        )

    def test_should_fail_refresh_when_interconnect_name_not_found(self):
        self.mock_ansible_module.params = PARAMS_FOR_REFRESH_WITHOUT_NAME

        SasInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=SasInterconnectModule.MSG_SAS_INTERCONNECT_NAME_REQUIRED)


if __name__ == '__main__':
    pytest.main([__file__])
