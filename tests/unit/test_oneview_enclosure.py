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

import mock
import pytest
import yaml

from copy import deepcopy
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import EnclosureModule

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_ENCLOSURE_NAME = 'Test-Enclosure'
PRIMARY_IP_ADDRESS = '172.18.1.13'
STANDBY_IP_ADDRESS = '172.18.1.14'

ENCLOSURE_FROM_ONEVIEW = dict(
    name='Encl1',
    uri='/a/path',
    applianceBayCount=2,
    uidState='Off',
    applianceBays=[
        dict(bayNumber=1, poweredOn=True, bayPowerState='Unknown'),
        dict(bayNumber=2, poweredOn=False, bayPowerState='Unknown')
    ],
    managerBays=[
        dict(bayNumber=1, uidState='On', bayPowerState='Unknown'),
        dict(bayNumber=2, uidState='Off', bayPowerState='Unknown')
    ],
    deviceBays=[
        dict(bayNumber=1, bayPowerState='Unknown'),
        dict(bayNumber=2, bayPowerState='Unknown')
    ],
    interconnectBays=[
        dict(bayNumber=1, bayPowerState='Unknown'),
        dict(bayNumber=2, bayPowerState='Unknown')
    ],
    supportDataCollectionState='Completed',
    activeOaPreferredIP=PRIMARY_IP_ADDRESS,
    standbyOaPreferredIP=STANDBY_IP_ADDRESS
)

ALL_ENCLOSURES = [dict(name='Encl3', uri='/a/path3', activeOaPreferredIP='172.18.1.3'),
                  dict(name='Encl2', uri='/a/path2', activeOaPreferredIP='172.18.1.2'),
                  ENCLOSURE_FROM_ONEVIEW]

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name='Encl1',
              hostname=PRIMARY_IP_ADDRESS,
              username='admin',
              password='password123')
)

PARAMS_FOR_PRESENT_NO_HOSTNAME = dict(
    config='config.json',
    state='present',
    data=dict(name='Encl1')
)

PARAMS_WITH_NEW_NAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              newName='OneView-Enclosure')
)

PARAMS_WITH_NEW_RACK_NAME = dict(
    config='config.json',
    state='present',
    data=dict(name='Encl1',
              rackName='Another-Rack-Name')
)

PARAMS_WITH_CALIBRATED_MAX_POWER = dict(
    config='config.json',
    state='present',
    data=dict(name='Encl1',
              calibratedMaxPower=1750)
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_ENCLOSURE_NAME)
)

PARAMS_FOR_RECONFIGURED = dict(
    config='config.json',
    state='reconfigured',
    data=dict(name=DEFAULT_ENCLOSURE_NAME)
)

PARAMS_FOR_REFRESH = dict(
    config='config.json',
    state='refreshed',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              refreshState='Refreshing')
)

PARAMS_FOR_BAY_POWER_ON = dict(
    config='config.json',
    state='appliance_bays_powered_on',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              bayNumber=2)
)

PARAMS_FOR_CREATE_CSR = dict(
    config='config.json',
    state='create_certificate_request',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              type='CertificateDtoV2',
              organization='HPE',
              organizationalUnit='IT',
              locality='Fort Collins',
              state='Colorado',
              country='US',
              commonName='e10-oa',
              bay_number=1)
)

PARAMS_FOR_GET_CSR = dict(
    config='config.json',
    state='get_certificate_request',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              bay_number=1)
)

PARAMS_FOR_IMPORT_CSR = dict(
    config='config.json',
    state='import_certificate_request',
    data=dict(name=DEFAULT_ENCLOSURE_NAME,
              type='CertificateDataV2',
              base64Data='certificate')
)

PARAMS_FOR_DATA_COL_SET = """
    config: "{{ config_file_path }}"
    state: support_data_collection_set
    data:
      name: 'Test-Enclosure'
      supportDataCollectionState: 'PendingCollection'
"""

PARAMS_FOR_INTERCONNECT_BAY_IPV4_RELEASE = """
    config: "{{ config_file_path }}"
    state: interconnect_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_DEVICE_BAY_IPV4_RELEASE = """
    config: "{{ config_file_path }}"
    state: device_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_UID_ON = """
    config: "{{ config_file_path }}"
    state: uid_on
    data:
      name: 'Test-Enclosure'
"""

PARAMS_FOR_UID_OFF = """
    config: "{{ config_file_path }}"
    state: uid_off
    data:
      name: 'Test-Enclosure'
"""

PARAMS_FOR_MANAGER_BAY_UID_ON = """
    config: "{{ config_file_path }}"
    state: manager_bays_uid_on
    data:
      name: 'Test-Enclosure'
      bayNumber: 2
"""

PARAMS_FOR_MANAGER_BAY_UID_OFF = """
    config: "{{ config_file_path }}"
    state: manager_bays_uid_off
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_MANAGER_BAY_POWER_STATE_E_FUSE = """
    config: "{{ config_file_path }}"
    state: manager_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_MANAGER_BAY_POWER_STATE_RESET = """
    config: "{{ config_file_path }}"
    state: manager_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_APPLIANCE_BAY_POWER_STATE_E_FUSE = """
    config: "{{ config_file_path }}"
    state: appliance_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_DEVICE_BAY_POWER_STATE_E_FUSE = """
    config: "{{ config_file_path }}"
    state: device_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_DEVICE_BAY_POWER_STATE_RESET = """
    config: "{{ config_file_path }}"
    state: device_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 1
"""

PARAMS_FOR_INTERCONNECT_BAY_POWER_STATE_E_FUSE = """
    config: "{{ config_file_path }}"
    state: interconnect_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 2
"""


@pytest.mark.resource(TestEnclosureModule='enclosures')
class TestEnclosureModule(OneViewBaseTest):
    def test_should_create_new_enclosure(self):
        self.resource.get_by_name.return_value = []
        self.resource.get_by_hostname.return_value = []

        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.add.return_value = self.resource
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureModule.MSG_CREATED,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_should_fail_create_new_enclosure(self):
        self.resource.get_by_name.return_value = []
        self.resource.get_by_hostname.return_value = []
        self.resource.add.return_value = []
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_ENCLOSURE_REQUIRED_FIELDS)

    def test_should_not_update_when_no_changes_by_primary_ip_key(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.get_by_hostname.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=EnclosureModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_should_not_update_when_no_changes_by_standby_ip_key(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.get_by_hostname.return_value = self.resource

        params = deepcopy(PARAMS_FOR_PRESENT)
        params['data']['hostname'] = STANDBY_IP_ADDRESS
        self.mock_ansible_module.params = params

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=EnclosureModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_should_not_update_when_no_changes_by_name_key(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.get_by_hostname.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT_NO_HOSTNAME

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=EnclosureModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_update_when_data_has_new_name(self):
        updated_data = ENCLOSURE_FROM_ONEVIEW.copy()
        updated_data['name'] = 'Test-Enclosure-Renamed'

        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.get_by_hostname.return_value = self.resource

        updated_obj = self.resource.copy()
        updated_obj.data = updated_data
        self.resource.patch.return_value = updated_obj

        self.mock_ansible_module.params = PARAMS_WITH_NEW_NAME

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureModule.MSG_UPDATED,
            ansible_facts=dict(enclosure=self.resource.data)
        )

    def test_update_when_data_has_new_rack_name(self):
        updated_data = ENCLOSURE_FROM_ONEVIEW.copy()
        updated_data['rackName'] = 'Another-Rack-Name'

        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        updated_obj = self.resource.copy()
        updated_obj.data = updated_data
        self.resource.patch.return_value = updated_obj

        self.mock_ansible_module.params = PARAMS_WITH_NEW_RACK_NAME

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureModule.MSG_UPDATED,
            ansible_facts=dict(enclosure=self.resource.data)
        )

    def test_replace_name_for_new_enclosure(self):
        self.resource.get_by_name.return_value = []
        self.resource.get_by_hostname.return_value = []
        self.resource.get_all.return_value = []

        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.add.return_value = self.resource

        self.resource.patch.return_value = []

        params_ansible = deepcopy(PARAMS_FOR_PRESENT)
        params_ansible['data']['name'] = 'Encl1-Renamed'
        self.mock_ansible_module.params = params_ansible

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with("replace", "/name", "Encl1-Renamed")

    def test_replace_name_for_existent_enclosure(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_NEW_NAME

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with("replace", "/name", "OneView-Enclosure")

    def test_replace_rack_name_for_new_enclosure(self):
        updated_data = ENCLOSURE_FROM_ONEVIEW.copy()
        updated_data['rackName'] = 'Another-Rack-Name'

        self.resource.get_by_name.return_value = []
        self.resource.get_by_hostname.return_value = []
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.add.return_value = self.resource
        self.resource.patch.return_value = updated_data

        params_ansible = deepcopy(PARAMS_FOR_PRESENT)
        params_ansible['data']['rackName'] = 'Another-Rack-Name'
        self.mock_ansible_module.params = params_ansible

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(
            "replace", "/rackName", "Another-Rack-Name")

    def test_replace_rack_name_for_existent_enclosure(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_NEW_RACK_NAME

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(
            "replace", "/rackName", "Another-Rack-Name")

    def test_update_calibrated_max_power_for_existent_enclosure(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = []

        self.mock_ansible_module.params = PARAMS_WITH_CALIBRATED_MAX_POWER

        EnclosureModule().run()

        self.resource.update_environmental_configuration.assert_called_once_with(
            {"calibratedMaxPower": 1750})

    def test_should_remove_enclosure(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureModule.MSG_DELETED
        )

    def test_should_do_nothing_when_enclosure_not_exist(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=EnclosureModule.MSG_ALREADY_ABSENT
        )

    def test_should_reconfigure_enclosure(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.update_configuration.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_RECONFIGURED
        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EnclosureModule.MSG_RECONFIGURED,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW)
        )

    def test_should_fail_when_enclosure_not_exist(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_RECONFIGURED
        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_ENCLOSURE_NOT_FOUND)

    def test_should_fail_when_name_is_not_in_data(self):
        self.resource.get_by_name.return_value = []

        params = deepcopy(PARAMS_FOR_RECONFIGURED)
        del params['data']['name']

        self.mock_ansible_module.params = params
        EnclosureModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=EnclosureModule.MSG_ENCLOSURE_NOT_FOUND)

    def test_should_refresh_enclosure(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.get.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_REFRESH

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_REFRESHED
        )

    def test_should_power_on_appliance_bays(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_BAY_POWER_ON

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/applianceBays/2/power',
                                                    value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_APPLIANCE_BAY_POWERED_ON
        )

    def test_should_not_power_on_when_state_is_already_on(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_do_nothing = deepcopy(PARAMS_FOR_BAY_POWER_ON)
        params_power_on_do_nothing['data']['bayNumber'] = 1
        self.mock_ansible_module.params = params_power_on_do_nothing

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_APPLIANCE_BAY_ALREADY_POWERED_ON
        )

    def test_should_fail_when_appliance_bay_not_found_power_on(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = deepcopy(PARAMS_FOR_BAY_POWER_ON)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_appliance_bays_power_on(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, applianceBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = PARAMS_FOR_BAY_POWER_ON

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_turn_on_uid(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_UID_ON)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/uidState',
                                                    value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_UID_POWERED_ON
        )

    def test_should_not_set_to_on_when_it_is_already_on(self):
        enclosure_uid_on = dict(ENCLOSURE_FROM_ONEVIEW, uidState='On')
        self.resource.data = enclosure_uid_on

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_UID_ON)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=enclosure_uid_on),
            msg=EnclosureModule.MSG_UID_ALREADY_POWERED_ON
        )

    def test_should_turn_off_uid(self):
        enclosure_uid_on = dict(ENCLOSURE_FROM_ONEVIEW, uidState='On')
        self.resource.data = enclosure_uid_on
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_UID_OFF)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/uidState',
                                                    value='Off')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=enclosure_uid_on),
            msg=EnclosureModule.MSG_UID_POWERED_OFF
        )

    def test_should_not_set_to_off_when_it_is_already_off(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_UID_OFF)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_UID_ALREADY_POWERED_OFF
        )

    def test_should_turn_on_uid_manager_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_ON)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/managerBays/2/uidState',
                                                    value='On')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_MANAGER_BAY_UID_ON
        )

    def test_should_not_set_to_on_when_state_already_on(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_manager_bay_uid = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_ON)
        params_manager_bay_uid['data']['bayNumber'] = '1'

        self.mock_ansible_module.params = params_manager_bay_uid

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_MANAGER_BAY_UID_ALREADY_ON
        )

    def test_should_fail_when_manager_bay_not_found(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_ON)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_manager_bays_uid_on(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, managerBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_ON)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_turn_off_uid_manager_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_OFF)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/managerBays/1/uidState',
                                                    value='Off')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_MANAGER_BAY_UID_OFF
        )

    def test_should_not_set_to_off_when_state_already_off(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_manager_bay_uid = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_OFF)
        params_manager_bay_uid['data']['bayNumber'] = '2'

        self.mock_ansible_module.params = params_manager_bay_uid

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_MANAGER_BAY_UID_ALREADY_OFF
        )

    def test_should_fail_when_manager_bay_not_found_uid_off(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_OFF)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_manager_bays_uid_off(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, managerBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_UID_OFF)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_perform_an_e_fuse_manager_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        updated_resource = self.resource.copy()
        updated_resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = updated_resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/managerBays/1/bayPowerState',
                                                    value='E-Fuse')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_MANAGER_BAY_POWER_STATE_E_FUSED
        )

    def test_should_fail_when_manager_bay_not_found_e_fuse(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_POWER_STATE_E_FUSE)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_manager_bays_e_fuse(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, managerBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_reset_manager_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_POWER_STATE_RESET)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/managerBays/1/bayPowerState',
                                                    value='Reset')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_MANAGER_BAY_POWER_STATE_RESET
        )

    def test_should_fail_when_manager_bay_not_found_power_reset(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_POWER_STATE_RESET)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_manager_bays_reset(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, managerBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_MANAGER_BAY_POWER_STATE_RESET)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_perform_an_e_fuse_appliance_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_APPLIANCE_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/applianceBays/1/bayPowerState',
                                                    value='E-Fuse')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_APPLIANCE_BAY_POWER_STATE_E_FUSED
        )

    def test_should_fail_when_appliance_bay_not_found_appliance_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_APPLIANCE_BAY_POWER_STATE_E_FUSE)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_appliance_bays_e_fuse(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, applianceBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_APPLIANCE_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_perform_an_e_fuse_device_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/deviceBays/1/bayPowerState',
                                                    value='E-Fuse')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_DEVICE_BAY_POWER_STATE_E_FUSED
        )

    def test_should_fail_when_device_bay_not_found_e_fuse(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_POWER_STATE_E_FUSE)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_device_bays_e_fuse(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, deviceBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_reset_device_bay(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_POWER_STATE_RESET)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/deviceBays/1/bayPowerState',
                                                    value='Reset')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_DEVICE_BAY_POWER_STATE_RESET
        )

    def test_should_fail_when_device_bay_not_found_reset(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_POWER_STATE_RESET)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_device_bays_reset(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, deviceBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_POWER_STATE_RESET)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_perform_an_e_fuse_interconnect(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_INTERCONNECT_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/interconnectBays/2/bayPowerState',
                                                    value='E-Fuse')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_INTERCONNECT_BAY_POWER_STATE_E_FUSE
        )

    def test_should_fail_when_interconnect_bay_not_found_e_fuse(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_INTERCONNECT_BAY_POWER_STATE_E_FUSE)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_interconnect_bays_e_fuse(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, interconnectBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_INTERCONNECT_BAY_POWER_STATE_E_FUSE)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_remove_ipv4_device_bays(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW
        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_IPV4_RELEASE)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='remove',
                                                    path='/deviceBays/1/ipv4Setting',
                                                    value='')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_DEVICE_BAY_IPV4_SETTING_REMOVED
        )

    def test_should_remove_ipv4_interconnect_bays(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_INTERCONNECT_BAY_IPV4_RELEASE)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='remove',
                                                    path='/interconnectBays/1/ipv4Setting',
                                                    value='')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_INTERCONNECT_BAY_IPV4_SETTING_REMOVED
        )

    def test_should_fail_when_device_bay_not_found_ipv4_release(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_IPV4_RELEASE)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_device_bays_ipv4_release(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, deviceBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_IPV4_RELEASE)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_interconnect_bay_not_found_ipv4(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        params_power_on_not_found_bay = yaml.safe_load(PARAMS_FOR_DEVICE_BAY_IPV4_RELEASE)
        params_power_on_not_found_bay['data']['bayNumber'] = 3
        self.mock_ansible_module.params = params_power_on_not_found_bay

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_fail_when_there_are_not_interconnect_bays_ipv4(self):
        enclosure_without_appliance_bays = dict(ENCLOSURE_FROM_ONEVIEW, interconnectBays=[])
        self.resource.data = enclosure_without_appliance_bays

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_INTERCONNECT_BAY_IPV4_RELEASE)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=EnclosureModule.MSG_BAY_NOT_FOUND)

    def test_should_set_state(self):
        self.resource.data = ENCLOSURE_FROM_ONEVIEW

        self.resource.patch.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DATA_COL_SET)

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/supportDataCollectionState',
                                                    value='PendingCollection')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_SUPPORT_DATA_COLLECTION_STATE_SET
        )

    def test_should_not_set_state_when_it_is_already_on_desired_state(self):
        enclosure_uid_on = dict(ENCLOSURE_FROM_ONEVIEW, supportDataCollectionState='PendingCollection')
        self.resource.data = enclosure_uid_on

        self.mock_ansible_module.params = yaml.safe_load(PARAMS_FOR_DATA_COL_SET)

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=enclosure_uid_on),
            msg=EnclosureModule.MSG_SUPPORT_DATA_COLLECTION_STATE_ALREADY_SET
        )

    def test_update_scopes_when_different(self):
        params_to_scope = deepcopy(PARAMS_FOR_PRESENT_NO_HOSTNAME)
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = deepcopy(PARAMS_FOR_PRESENT_NO_HOSTNAME)['data']
        resource_data['uri'] = 'rest/enclosures/fake'
        resource_data['scopeUris'] = []

        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj

        EnclosureModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=patch_return),
            msg=EnclosureModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = deepcopy(PARAMS_FOR_PRESENT_NO_HOSTNAME)
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        self.resource.data = params_to_scope['data']

        EnclosureModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure=params_to_scope['data']),
            msg=EnclosureModule.MSG_ALREADY_PRESENT
        )

    def test_should_create_new_certificate_signing_request(self):
        self.resource.generate_csr.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_CREATE_CSR

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_CREATE_CERTIFICATE_REQUEST
        )

    def test_should_get_previous_certificate_signing_request(self):
        self.resource.get_csr.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_GET_CSR

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_GET_CERTIFICATE_REQUEST
        )

    def test_should_import_certificate_signing_request(self):
        self.resource.import_certificate.return_value = ENCLOSURE_FROM_ONEVIEW

        self.mock_ansible_module.params = PARAMS_FOR_IMPORT_CSR

        EnclosureModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(enclosure=ENCLOSURE_FROM_ONEVIEW),
            msg=EnclosureModule.MSG_IMPORT_CERTIFICATE_REQUEST
        )


if __name__ == '__main__':
    pytest.main([__file__])
