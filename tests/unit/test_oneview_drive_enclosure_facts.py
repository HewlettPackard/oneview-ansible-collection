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

import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import DriveEnclosureFactsModule

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Drive-Enclosure",
    options=[]
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    uri="/rest/drive-enclosures/c6bf9af9-48e7-4236-b08a-77684dc258a5",
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test-Drive-Enclosure",
    options=["port_map"]
)

PRESENT_DRIVE_ENCLOSURES = [{
    "name": "Test-Drive-Enclosure",
    "uri": "/rest/drive-enclosures/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]

DRIVE_ENCLOSURE_PORT_MAP = {
    "type": "DriveEnclosurePortMap",
    "deviceSlots":[{
        "slotNumber": "1",
        "physicalPorts": [
            {
                "physicalInterconnectUri": "/rest/sas-interconnects/2M220102SL",
                "physicalInterconnectPortNumber": "1"
            }
        ]
    }]
}


@pytest.mark.resource(TestDriveEnclosureFactsModule='drive_enclosures')
class TestDriveEnclosureFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_drive_enclosures(self):
        self.resource.get_all.return_value = PRESENT_DRIVE_ENCLOSURES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=(PRESENT_DRIVE_ENCLOSURES))
        )

    def test_get_drive_enclosure_by_name_without_matching_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=[])
        )

    def test_should_get_drive_enclosure_by_name(self):
        self.resource.data = PRESENT_DRIVE_ENCLOSURES[0]
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=(PRESENT_DRIVE_ENCLOSURES))

        )

    def test_should_get_drive_enclosure_by_uri(self):
        self.resource.data = PRESENT_DRIVE_ENCLOSURES[0]
        self.resource.get_by_uri.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=(PRESENT_DRIVE_ENCLOSURES))

        )

    def test_should_get_drive_enclosure_by_name_with_options(self):
        self.resource.data = PRESENT_DRIVE_ENCLOSURES[0]
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_by_uri.return_value = self.resource
        self.resource.get_by.return_value = PRESENT_DRIVE_ENCLOSURES

        self.resource.get_port_map.return_value = DRIVE_ENCLOSURE_PORT_MAP

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=PRESENT_DRIVE_ENCLOSURES,
                               port_map=DRIVE_ENCLOSURE_PORT_MAP)
        )


if __name__ == '__main__':
    pytest.main([__file__])
