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
import yaml

from copy import deepcopy
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasLogicalInterconnectModule

SAS_LI_FROM_ONEVIEW = dict(
    name="SAS_LI",
    uri="/rest/sas-logical-interconnect/197f33a3",
    description="LI description",
    refreshState="NotRefreshing"
)
PARAMS_FOR_COMPLIANCE_CHECK = dict(
    config='config.json',
    state='compliance',
    data=dict(name='SAS_LI')
)
PARAMS_FOR_APPLY_CONFIGURATION = dict(
    config='config.json',
    state='apply_configuration',
    data=dict(name='SAS_LI')
)
PARAMS_FOR_FIRMWARE_INSTALL = dict(
    config='config.json',
    state='install_firmware',
    data=dict(name='SAS_LI',
              firmware=dict(command="Stage",
                            force="false",
                            sppUri="/rest/firmware-drivers/afdaf-adsf")
        )
)
PARAMS_FOR_REPLACE_DR_ENCL = dict(
    config='config.json',
    state='replace_drive_enclosure',
    data=dict(name='SAS_LI',driveReplaceConfig=dict(oldSerialNumber="SN1100",
                                                    newSerialNumber= "SN1101")
            )
        )
PARAMS_WITH_NO_CONFIG_FIRMWARE = dict(
    config='config.json',
    state='install_firmware',
    data=dict(name='SAS_LI')
)
PARAMS_WITH_NO_CONFIG_REPLACE_DR_ENC = dict(
    config='config.json',
    state='replace_drive_enclosure',
    data=dict(name='SAS_LI')
)


@pytest.mark.resource(TestSasLogicalInterconnectModule='sas_logical_interconnects')
class TestSasLogicalInterconnectModule(OneViewBaseTest):
    def test_should_check_compliance(self):
        self.resource.data = SAS_LI_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_COMPLIANCE_CHECK
        self.resource.update_compliance.return_value = self.resource.data

        SasLogicalInterconnectModule().run()

        self.resource.update_compliance.assert_called_once()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_interconnect=self.resource.data),
            msg=SasLogicalInterconnectModule.MSG_CONSISTENT
        )

    def test_should_apply_configuration(self):
        self.resource.data = SAS_LI_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_APPLY_CONFIGURATION
        self.resource.update_configuration.return_value = self.resource.data

        SasLogicalInterconnectModule().run()

        self.resource.update_configuration.assert_called_once()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_interconnect=self.resource.data),
            msg=SasLogicalInterconnectModule.MSG_CONFIGURATION_UPDATED
        )

    def test_should_install_firmware(self):
        self.resource.data = SAS_LI_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_FIRMWARE_INSTALL
        self.resource.update_firmware.return_value = self.resource.data

        SasLogicalInterconnectModule().run()

        self.resource.update_firmware.assert_called_once_with(PARAMS_FOR_FIRMWARE_INSTALL["data"]["firmware"])
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(li_firmware=self.resource.data),
            msg=SasLogicalInterconnectModule.MSG_FIRMWARE_INSTALLED
        )

    def test_should_fail_if_no_config_for_install_firmware(self):
        self.resource.data = SAS_LI_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_WITH_NO_CONFIG_FIRMWARE
        self.resource.update_firmware.return_value = self.resource.data

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=SasLogicalInterconnectModule.MSG_NO_OPTIONS_PROVIDED)

    def test_should_replace_drive_enclosure(self):
        self.resource.data = SAS_LI_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_REPLACE_DR_ENCL
        self.resource.replace_drive_enclosure.return_value = self.resource.data

        SasLogicalInterconnectModule().run()

        self.resource.replace_drive_enclosure.assert_called_once_with(PARAMS_FOR_REPLACE_DR_ENCL["data"]["driveReplaceConfig"])
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(drive_replacement_output=self.resource.data),
            msg=SasLogicalInterconnectModule.MSG_DRIVE_ENCLOSURE_REPLACED
        )

    def test_should_fail_if_no_config_for_replace_drive_enclosure(self):
        self.resource.data = SAS_LI_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_WITH_NO_CONFIG_REPLACE_DR_ENC
        self.resource.update_firmware.return_value = self.resource.data

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=SasLogicalInterconnectModule.MSG_NO_OPTIONS_PROVIDED)

    def test_should_not_patch_if_no_li_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_REPLACE_DR_ENCL

        SasLogicalInterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=SasLogicalInterconnectModule.MSG_NOT_FOUND)


if __name__ == '__main__':
    pytest.main([__file__])
