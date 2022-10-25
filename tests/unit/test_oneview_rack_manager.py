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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import RackManagerModule

YAML_RACK_MANAGER_PRESENT = """
        config: "{{ config }}"
        state: present
        data:
             hostname : "1.2.3.4"
             username : "dcs"
             password : "dcs"
             force : false
          """

YAML_RACK_MANAGER_REFRESH = """
        config: "{{ config }}"
        state: refresh_state_set
        data:
             name : "1.2.3.4"
          """

YAML_RACK_MANAGER_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name : "172.18.6.15"
        """


@pytest.mark.resource(TestRackManagerModule='rack_managers')
class TestRackManagerModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_add_new_rack_manager(self):
        self.resource.get_by_name.return_value = []
        self.resource.data = {"name": "name"}
        self.resource.add.return_value = self.resource

        self.mock_ansible_module.params = yaml.safe_load(YAML_RACK_MANAGER_PRESENT)

        RackManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackManagerModule.MSG_ADDED,
            ansible_facts=dict(rack_manager={"name": "name"})
        )

    def test_should_not_add_when_it_already_exists(self):
        self.resource.data = {"name": "name"}

        self.mock_ansible_module.params = yaml.safe_load(YAML_RACK_MANAGER_PRESENT)

        RackManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RackManagerModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(rack_manager={"name": "name"})
        )

    def test_should_refresh_rack_manager(self):
        self.resource.data = {"name": "name"}
        self.resource.get_by_name.return_value = self.resource

        self.current_resource = self.resource

        self.mock_ansible_module.params = yaml.safe_load(YAML_RACK_MANAGER_REFRESH)

        RackManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackManagerModule.MSG_RACK_MANAGER_REFRESHED,
            ansible_facts=dict(rack_manager={"name": "name"})
        )

    def test_should_fail_when_set_refresh_state_and_rack_manager_was_not_found(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = yaml.safe_load(YAML_RACK_MANAGER_REFRESH)

        RackManagerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=RackManagerModule.MSG_RACK_MANAGER_NOT_FOUND)


    def test_should_fail_with_missing_name_attribute(self):
        self.mock_ansible_module.params = {"state": "absent",
                                           "config": "config",
                                           "data":
                                               {"field": "invalid"}}

        RackManagerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=RackManagerModule.MSG_MANDATORY_FIELD_MISSING.format('data.name'))


    def test_should_remove_rack_manager(self):
        self.resource.data = {'name': 'name'}

        self.mock_ansible_module.params = yaml.safe_load(YAML_RACK_MANAGER_ABSENT)

        RackManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RackManagerModule.MSG_DELETED
        )

    def test_should_do_nothing_when_rack_manager_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = yaml.safe_load(YAML_RACK_MANAGER_ABSENT)

        RackManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RackManagerModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
