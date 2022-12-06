#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2022) Hewlett Packard Enterprise Development LP
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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SanManagerModule

SAN_MANAGER_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(
        providerDisplayName="Brocade FOS Switch",
        connectionInfo=[
            dict(name="Host",
                 value="172.18.19.39"),
            dict(name="Username",
                 value="dcs"),
            dict(name="Password",
                 value="dcs"),
            dict(name="UseHttps",
                 value="true")]))

SAN_MANAGER_UPDATE = dict(
    config='config.json',
    state='present',
    data=dict(
        name="172.18.19.39",
        connectionInfo=[
            dict(name="Host",
                 value="172.18.19.39"),
            dict(name="Username",
                 value="dcs"),
            dict(name="Password",
                 value="dcs"),
            dict(name="UseHttps",
                 value="true")]))

SAN_MANAGER_PASSWORD_UPDATE = dict(
    config='config.json',
    state='present',
    data=dict(
        name="172.18.19.39",
        connectionInfo=[
            dict(name="Host",
                 value="172.18.19.39"),
            dict(name="Username",
                 value="dcs"),
            dict(name="Password",
                 value="dcs",
                 updatePassword=True),
            dict(name="UseHttps",
                 value="true")]))

SAN_MANAGER_REFRESH = dict(
    config='config.json',
    state='refresh_state_set',
    data=dict(name="172.18.19.39",
              refreshState="RefreshPending"))

SAN_MANAGER_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name="172.18.19.39"))


@pytest.mark.resource(TestSanManagerModule='san_managers')
class TestSanManagerModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_add_new_san_manager(self):
        self.resource.get_by_name.return_value = []
        self.resource.data = {"name": "name"}
        self.resource.add.return_value = self.resource
        self.mock_ov_client.san_providers.add.return_value = self.resource.data
        self.mock_ov_client.san_managers.get_by_provider_display_name.return_value = None
        self.mock_ansible_module.params = SAN_MANAGER_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_ADDED,
            ansible_facts=dict(san_managers={"name": "name"})
        )

    def test_should_not_add_when_it_already_exists(self):
        self.resource.data = {"name": "name"}

        self.resource.add.return_value = self.resource
        self.mock_ov_client.san_providers.add.return_value = self.resource.data
        self.mock_ov_client.san_managers.get_by_provider_display_name.return_value = self.resource
        self.mock_ansible_module.params = SAN_MANAGER_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(san_managers={"name": "name"})
        )

    def test_should_refresh_san_manager(self):
        self.resource.data = {"name": "name", "uri": "resourceuri", "refreshState": "Stable"}
        self.resource.get_by_name.return_value = self.resource
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = SAN_MANAGER_REFRESH

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_SAN_MANAGER_REFRESHED,
            ansible_facts=dict(san_managers={"name": "name", "uri": "resourceuri", "refreshState": "Stable"})
        )

    def test_should_update_san_manager(self):
        self.resource.data = {"name": "name", "uri": "resourceuri", "connectionInfo": []}
        self.resource.get_by_name.return_value = self.resource
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = SAN_MANAGER_UPDATE

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_SAN_MANAGER_UPDATED,
            ansible_facts=dict(san_managers={"name": "name", "uri": "resourceuri", "connectionInfo": []})
        )

    def test_should_not_update_san_manager_for_same_data(self):
        self.resource.data = {"name": "172.18.19.39", "uri": "resourceuri", "connectionInfo": [{"name":"Host", "value":"172.18.19.39"},
                             {"name":"Username", "value":"dcs"}, {"name":"Password", "value":"dcs"}, {"name":"UseHttps", "value":"true"}]}
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = SAN_MANAGER_UPDATE

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(san_managers=self.resource.data)
        )

    def test_should_update_if_update_password_if_update_flag_set(self):
        self.resource.data = {"name": "172.18.19.39", "uri": "resourceuri", "connectionInfo": [{"name":"Host", "value":"172.18.19.39"},
                             {"name":"Username", "value":"dcs"}, {"name":"Password", "value":""}, {"name":"UseHttps", "value":"true"}]}
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = SAN_MANAGER_PASSWORD_UPDATE

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_SAN_MANAGER_UPDATED,
            ansible_facts=dict(san_managers=self.resource.data)
        )

    def test_should_remove_san_manager(self):
        self.resource.data = {'name': 'name'}

        self.mock_ansible_module.params = SAN_MANAGER_ABSENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_DELETED
        )

    def test_should_do_nothing_when_san_manager_is_already_absent(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = SAN_MANAGER_ABSENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_ALREADY_ABSENT
        )

    def test_present_should_fail_with_missing_connectionInfo_attribute(self):
        self.mock_ansible_module.params = {"state": "present",
                                           "config": "config",
                                           "data":
                                               {"field": "invalid"}}

        SanManagerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY, msg=SanManagerModule.MSG_MANDATORY_FIELD_MISSING.format('data.connectionInfo'))

    def test_present_should_fail_with_missing_providerDisplayName_attribute(self):
        self.mock_ansible_module.params = {"state": "present",
                                           "config": "config",
                                           "data":
                                               {"field": "invalid",
                                                "connectionInfo": "some_data"}}

        SanManagerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            exception=mock.ANY, msg=SanManagerModule.MSG_MANDATORY_FIELD_MISSING.format('data.providerDisplayName'))


if __name__ == '__main__':
    pytest.main([__file__])
