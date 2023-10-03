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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasLogicalJbodModule

SAS_JBOD_FROM_ONEVIEW = dict(
    name="SASJbod",
    uri="/rest/sas-logical-jbods/197f33a3",
    description="Jbod description",
    refreshState="NotRefreshing",
    eraseData="true",
    clearMetaData="false"
)
PARAMS_FOR_CREATE = dict(
    config='config.json',
    state='present',
    data=dict(name='SASJbod',
              numPhysicalDrives=1,
              eraseData="true",
              driveEnclosureUris=["some/uri"])
)
PARAMS_FOR_DELETE = dict(
    config='config.json',
    state='absent',
    data=dict(name='SASJbod')
)
PARAMS_FOR_NAME_CHANGE = dict(
    config='config.json',
    state='change_name',
    data=dict(name='SASJbod',
              newName="NewJbodName")
)
PARAMS_FOR_SAME_NAME_CHANGE = dict(
    config='config.json',
    state='change_name',
    data=dict(name='SASJbod',
              newName="SASJbod")
)
PARAMS_FOR_DESCRIPTION_CHANGE = dict(
    config='config.json',
    state='change_description',
    data=dict(name='SASJbod',
              newDescription="New Description for jbod")
)
PARAMS_FOR_SAME_DESCRIPTION_CHANGE = dict(
    config='config.json',
    state='change_description',
    data=dict(name='SASJbod',
              newDescription="Jbod description")
)
PARAMS_FOR_ERASE_DATA = dict(
    config='config.json',
    state='erase_data',
    data=dict(name='SASJbod')
)
PARAMS_FOR_CLEAR_METADATA = dict(
    config='config.json',
    state='clear_metadata',
    data=dict(name='SASJbod')
)


@pytest.mark.resource(TestSasLogicalJbodModule='sas_logical_jbods')
class TestSasLogicalJbodModule(OneViewBaseTest):
    def test_should_create_sas_logical_jbod(self):
        self.resource.get_by_name.return_value = None
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.create.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_CREATE

        SasLogicalJbodModule().run()

        self.resource.create.assert_called_once_with(PARAMS_FOR_CREATE["data"])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_jbod=SAS_JBOD_FROM_ONEVIEW),
            msg=SasLogicalJbodModule.MSG_JBOD_CREATED
        )

    def test_should_not_create_if_jbod_exists(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_CREATE

        SasLogicalJbodModule().run()

        self.resource.create.not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbod=SAS_JBOD_FROM_ONEVIEW),
            msg=SasLogicalJbodModule.MSG_JBOD_ALREADY_EXISTS
        )

    def test_should_delete_jbod(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_DELETE

        SasLogicalJbodModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg="Resource deleted successfully."
        )

    def test_should_not_delete_if_jbod_doesnot_exist(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_DELETE

        SasLogicalJbodModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg="Resource is already absent."
        )

    def test_should_do_patch_to_change_name_of_jbod(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_NAME_CHANGE
        resource_after_patch = dict(SAS_JBOD_FROM_ONEVIEW, name=PARAMS_FOR_NAME_CHANGE["data"]["newName"])
        self.resource.patch.return_value.data = resource_after_patch

        SasLogicalJbodModule().run()

        self.resource.patch.assert_called_once_with(operation="replace",
                                                    path="/name",
                                                    value=PARAMS_FOR_NAME_CHANGE["data"]["newName"])
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_jbod=resource_after_patch),
            msg=SasLogicalJbodModule.MSG_JBOD_NAME_CHANGED
        )

    def test_should_not_patch_name_if_name_is_same(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_SAME_NAME_CHANGE

        SasLogicalJbodModule().run()

        self.resource.patch.had_not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasLogicalJbodModule.MSG_JBOD_NAME_NOT_CHANGED,
            ansible_facts=dict(sas_logical_jbod=self.resource.data)
        )

    def test_should_do_patch_to_change_description_of_jbod(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_DESCRIPTION_CHANGE
        resource_after_patch = dict(SAS_JBOD_FROM_ONEVIEW, description=PARAMS_FOR_DESCRIPTION_CHANGE["data"]["newDescription"])
        self.resource.patch.return_value.data = resource_after_patch

        SasLogicalJbodModule().run()

        self.resource.patch.assert_called_once_with(operation="replace",
                                                    path="/description",
                                                    value=PARAMS_FOR_DESCRIPTION_CHANGE["data"]["newDescription"])
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_jbod=resource_after_patch),
            msg=SasLogicalJbodModule.MSG_JBOD_DESCRIPTION_CHANGED
        )

    def test_should_not_patch_description_if_description_is_same(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_SAME_DESCRIPTION_CHANGE

        SasLogicalJbodModule().run()

        self.resource.patch.had_not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasLogicalJbodModule.MSG_JBOD_DESCRIPTION_NOT_CHANGED,
            ansible_facts=dict(sas_logical_jbod=self.resource.data)
        )

    def test_should_do_patch_for_disabling_drive_sanitize_option(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_ERASE_DATA
        resource_after_patch = dict(SAS_JBOD_FROM_ONEVIEW, eraseData="false")
        self.resource.patch.return_value.data = resource_after_patch

        SasLogicalJbodModule().run()

        self.resource.patch.assert_called_once_with(operation="replace",
                                                    path="/eraseData",
                                                    value="false")
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_jbod=resource_after_patch),
            msg=SasLogicalJbodModule.MSG_DISABLED_DRIVE_SANITIZE_OPTION
        )

    def test_should_not_do_patch_if_drive_sanitize_option_already_disabled(self):
        self.resource.data = dict(SAS_JBOD_FROM_ONEVIEW, eraseData="false")
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_ERASE_DATA

        SasLogicalJbodModule().run()

        self.resource.patch.had_not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasLogicalJbodModule.MSG_DRIVE_SANITIZE_OPTION_ALREADY_DISABLED,
            ansible_facts=dict(sas_logical_jbod=self.resource.data)
        )

    def test_should_do_patch_for_clearing_metadata(self):
        self.resource.data = SAS_JBOD_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_CLEAR_METADATA
        self.resource.patch.return_value.data = SAS_JBOD_FROM_ONEVIEW

        SasLogicalJbodModule().run()

        self.resource.patch.assert_called_once_with(operation="replace",
                                                    path="/clearMetadata",
                                                    value="true")
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_jbod=SAS_JBOD_FROM_ONEVIEW),
            msg=SasLogicalJbodModule.MSG_CLEARED_METADATA
        )

    def test_should_not_patch_if_no_jbod_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_CLEAR_METADATA

        SasLogicalJbodModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY,
                                                                   msg=SasLogicalJbodModule.MSG_JBOD_NOT_FOUND)


if __name__ == '__main__':
    pytest.main([__file__])
