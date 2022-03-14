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
from copy import deepcopy

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import FirmwareBundleModule

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_FIRMWARE_FILE_PATH = '/path/to/file.rpm'

DEFAULT_FIRMWARE_TEMPLATE = dict(
    bundleSize='4837926',
    bundleType='Hotfix',
    category='firmware-drivers',
    description='Provides firmware for the following drive model: MB1000GCWCV and MB4000GCWDC Drives',
    fwComponents=[dict(componentVersion='HPGH',
                       fileName='hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm',
                       name='Supplemental Update',
                       swKeyNameList=['hp-firmware-hdd-a1b08f8a6b'])]
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    file_path=DEFAULT_FIRMWARE_FILE_PATH
)

PARAMS_FOR_ADD_SIGNATURE = dict(
    config='config.json',
    state='add_signature',
    file_path=DEFAULT_FIRMWARE_FILE_PATH
)


@pytest.mark.resource(TestFirmwareBundleModule='firmware_bundles')
class TestFirmwareBundleModule(OneViewBaseTest):
    def test_should_upload_spp(self):
        self.resource.get_by_name.return_value = None
        self.resource.upload.return_value = deepcopy(DEFAULT_FIRMWARE_TEMPLATE)

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FirmwareBundleModule.MSG_ADDED,
            ansible_facts=dict(firmware_bundle=DEFAULT_FIRMWARE_TEMPLATE)
        )

    def test_should_not_upload_spp_when_already_present(self):
        self.resource.data = deepcopy(DEFAULT_FIRMWARE_TEMPLATE)
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FirmwareBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FirmwareBundleModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(firmware_bundle=DEFAULT_FIRMWARE_TEMPLATE)
        )

    def test_should_add_compsig(self):
        SPP_TEMPLATE = deepcopy(DEFAULT_FIRMWARE_TEMPLATE)
        SPP_TEMPLATE['signatureFileRequired'] = False
        SPP_TEMPLATE['resourceState'] = 'AddFailed'

        self.resource.data = SPP_TEMPLATE
        self.resource.get_by_name.return_value = self.resource
        self.resource.upload_compsig.return_value = DEFAULT_FIRMWARE_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_ADD_SIGNATURE

        FirmwareBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FirmwareBundleModule.MSG_ADD_SIG,
            ansible_facts=dict(compsig=DEFAULT_FIRMWARE_TEMPLATE)
        )

    def test_should_not_add_compsig_when_already_present(self):
        SPP_TEMPLATE = deepcopy(DEFAULT_FIRMWARE_TEMPLATE)
        SPP_TEMPLATE['signatureFileRequired'] = True
        SPP_TEMPLATE['resourceState'] = 'Created'
        self.resource.data = SPP_TEMPLATE
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_ADD_SIGNATURE

        FirmwareBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FirmwareBundleModule.MSG_SIG_ALREADY_PRESENT
        )

    def test_should_fail_to_add_compsig_when_hotfix_is_absent(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_ADD_SIGNATURE

        FirmwareBundleModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            failed=True,
            msg=FirmwareBundleModule.MSG_HOTFIX_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
