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
# import yaml

from copy import deepcopy
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import DriveEnclosureModule

DRIVE_ENCLOSURE_FROM_ONEVIEW = dict(
    name='DriveEncl1',
    uri='/a/path',
    powerState='Off',
    uidState='Off',
    hardResetState='Normal',
    driveBays=[
        dict(bayNumber=1, powerState="On", uri='/rest/drive-enclosures/abcd-defg'),
        dict(bayNumber=2, powerState="On", uri='/rest/drive-enclosures/xyz-dfg')
    ]
)
PARAMS_FOR_POWER_ON = dict(
    config='config.json',
    state='power_on',
    data=dict(name='DriveEncl1')
)
PARAMS_FOR_POWER_OFF = dict(
    config='config.json',
    state='power_off',
    data=dict(name='DriveEncl1')
)
PARAMS_FOR_UID_ON = dict(
    config='config.json',
    state='uid_on',
    data=dict(name='DriveEncl1')
)
PARAMS_FOR_UID_OFF = dict(
    config='config.json',
    state='uid_off',
    data=dict(name='DriveEncl1')
)
PARAMS_FOR_HARD_RESET = dict(
    config='config.json',
    state='hard_reset',
    data=dict(name='DriveEncl1')
)
PARAMS_FOR_REFRESH = dict(
    config='config.json',
    state='refreshed',
    data=dict(name='DriveEncl2',
              refreshState="RefreshPending")
)

PARAMS_WITHOUT_NAME = dict(
    config='config.json',
    state='refreshed',
    data=dict(refreshState="RefreshPending")
)


@pytest.mark.resource(TestDriveEnclosureModule='drive_enclosures')
class TestDriveEnclosureModule(OneViewBaseTest):
    def test_should_power_on_drive_enclosure(self):
        self.resource.data = DRIVE_ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_POWER_ON

        DriveEnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/powerState',
                                                    value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_DRIVE_ENCLOSURE_POWERED_ON
        )

    def test_should_not_power_on_when_state_is_already_on(self):
        drive_enclosure_power_on = dict(DRIVE_ENCLOSURE_FROM_ONEVIEW, powerState='On')
        self.resource.data = drive_enclosure_power_on

        params_power_on_do_nothing = deepcopy(PARAMS_FOR_POWER_ON)
        self.mock_ansible_module.params = params_power_on_do_nothing

        DriveEnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_DRIVE_ENCLOSURE_ALREADY_POWERED_ON
        )

    def test_should_power_off_drive_enclosure(self):
        drive_enclosure_power_on = dict(DRIVE_ENCLOSURE_FROM_ONEVIEW, powerState='On')
        self.resource.data = drive_enclosure_power_on
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_POWER_OFF

        DriveEnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/powerState',
                                                    value='Off')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DriveEnclosureModule.MSG_DRIVE_ENCLOSURE_POWERED_OFF,
            ansible_facts=dict(drive_enclosure=self.resource.data)
        )

    def test_should_not_power_off_when_state_is_already_off(self):
        self.resource.data = DRIVE_ENCLOSURE_FROM_ONEVIEW

        params_power_on_do_nothing = deepcopy(PARAMS_FOR_POWER_OFF)
        self.mock_ansible_module.params = params_power_on_do_nothing

        DriveEnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_DRIVE_ENCLOSURE_ALREADY_POWERED_OFF
        )

    def test_should_turn_on_uid(self):
        self.resource.data = DRIVE_ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_UID_ON

        DriveEnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/uidState',
                                                    value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_UID_POWERED_ON
        )

    def test_should_not_turn_uid_on_when_state_is_already_on(self):
        drive_enclosure_uid_on = dict(DRIVE_ENCLOSURE_FROM_ONEVIEW, uidState='On')
        self.resource.data = drive_enclosure_uid_on

        params_power_on_do_nothing = deepcopy(PARAMS_FOR_UID_ON)
        self.mock_ansible_module.params = params_power_on_do_nothing

        DriveEnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_UID_ALREADY_POWERED_ON
        )

    def test_should_turn_off_uid(self):
        drive_enclosure_uid_on = dict(DRIVE_ENCLOSURE_FROM_ONEVIEW, uidState='On')
        self.resource.data = drive_enclosure_uid_on
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_UID_OFF

        DriveEnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/uidState',
                                                    value='Off')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_UID_POWERED_OFF
        )

    def test_should_not_turn_uid_off_when_state_is_already_off(self):
        self.resource.data = DRIVE_ENCLOSURE_FROM_ONEVIEW

        params_power_on_do_nothing = deepcopy(PARAMS_FOR_UID_OFF)
        self.mock_ansible_module.params = params_power_on_do_nothing

        DriveEnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_UID_ALREADY_POWERED_OFF
        )

    def test_should_hard_reset_drive_enclosure(self):
        self.resource.data = DRIVE_ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_HARD_RESET

        DriveEnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/hardResetState',
                                                    value='Reset')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_HARD_RESET_DRIVE_ENCLOSURE
        )

    def test_should_refresh_drive_enclosure(self):
        self.resource.data = DRIVE_ENCLOSURE_FROM_ONEVIEW
        self.resource.refresh_state.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        DriveEnclosureModule().run()

        self.resource.refresh_state.assert_called_once_with({"refreshState": "RefreshPending"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_enclosure=self.resource.data),
            msg=DriveEnclosureModule.MSG_DRIVE_ENCLOSURE_REFRESHED
        )

    def test_refresh_should_fail_if_no_drive_enclosure_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        DriveEnclosureModule().run()

        self.resource.refresh_state.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=DriveEnclosureModule.MSG_DRIVE_ENCLOSURE_NOT_FOUND)

    def test_should_raise_exception_when_name_not_defined(self):
        self.mock_ansible_module.params = PARAMS_WITHOUT_NAME

        DriveEnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=DriveEnclosureModule.MSG_DRIVE_ENCLOSURE_NAME_REQUIRED)


if __name__ == '__main__':
    pytest.main([__file__])
