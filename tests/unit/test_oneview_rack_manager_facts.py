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

import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import RackManagerFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Rack Manager"
)

PARAMS_GET_BY_URI = dict(
    config='config.json',
    name="Test Rack Manager",
    uri="resource_uri"
)

PARAMS_GATHER_ALL_FACTS = dict(
    config='config.json',
    options=list(['chassis', 'partitions', 'managers'])
)

PARAMS_GATHER_CHASSIS_FACTS = dict(
    config='config.json',
    name="Test Rack Manager",
    options=list(['chassis'])
)

PARAMS_GATHER_ALL_FACTS_RACK_MANAGER = dict(
    config='config.json',
    name="Test Rack Manager",
    options=list(['chassis', 'partitions', 'managers', 'environmental_configuration', 'remote_support_settings'])
)


@pytest.mark.resource(TestRackManagerFactsModule='rack_managers')
class TestRackManagerFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_rack_managers(self):
        self.resource.get_all.return_value = {"name": "Rack Manager Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        RackManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(rack_managers=({"name": "Rack Manager Name"})),
        )

    def test_should_get_rack_manager_by_name(self):
        self.resource.data = {"name": "Test Rack Manager"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        RackManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(rack_managers=({"name": "Test Rack Manager"})),
        )

    def test_should_get_rack_manager_by_uri(self):
        self.resource.data = {"name": "Test Rack Manager", "uri": "resource_uri"}
        self.mock_ansible_module.params = PARAMS_GET_BY_URI

        RackManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                rack_managers=({"name": "Test Rack Manager", "uri": "resource_uri"})
            ),
        )

    def test_gather_facts_about_all_rack_managers(self):
        self.resource.get_all_chassis.return_value = {"name": "Chassis Name"}
        self.resource.get_all_partitions.return_value = {"name": "Partition Name"}
        self.resource.get_all_managers.return_value = {"name": "Managers Name"}
        self.resource.get_all.return_value = {"name": "Rack Manager Name"}
        self.mock_ansible_module.params = PARAMS_GATHER_ALL_FACTS

        RackManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                all_chassis=({"name": "Chassis Name"}),
                all_partitions=({"name": "Partition Name"}),
                all_managers=({"name": "Managers Name"}),
                rack_managers=({"name": "Rack Manager Name"}),
            ),
        )

    def test_gather_chassis_facts_about_a_rack_manager(self):
        self.resource.data = {"name": "Rack Manager Name"}
        self.resource.get_associated_chassis.return_value = {"category": "rack-managers", "members": [{"name": "chassis name"}]}
        self.current_resource = self.resource
        self.mock_ansible_module.params = PARAMS_GATHER_CHASSIS_FACTS

        RackManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                rack_manager_chassis=(
                    {"category": "rack-managers", "members": [{"name": "chassis name"}]}
                ),
                rack_managers=({"name": "Rack Manager Name"}),
            ),
        )

    def test_gather_all_facts_about_a_rack_manager(self):
        self.resource.data = {"name": "Rack Manager Name"}
        self.resource.get_associated_chassis.return_value = {"category": "rack-managers", "members": [{"name": "chassis name"}]}
        self.resource.get_associated_partitions.return_value = {"category": "rack-managers", "members": [{"name": "partition name"}]}
        self.resource.get_associated_managers.return_value = {"category": "rack-managers", "members": [{"name": "manager name"}]}
        self.resource.get_environmental_configuration.return_value = {"rackName": "Rack Name"}
        self.resource.get_remote_support_settings.return_value = {"type": "Remote Support Settings"}

        self.current_resource = self.resource
        self.mock_ansible_module.params = PARAMS_GATHER_ALL_FACTS_RACK_MANAGER

        RackManagerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                rack_manager_chassis=(
                    {"category": "rack-managers", "members": [{"name": "chassis name"}]}
                ),
                rack_manager_partitions=(
                    {
                        "category": "rack-managers",
                        "members": [{"name": "partition name"}],
                    }
                ),
                rack_manager_managers=(
                    {"category": "rack-managers", "members": [{"name": "manager name"}]}
                ),
                rack_manager_env_conf=({"rackName": "Rack Name"}),
                rack_manager_remote_support=({"type": "Remote Support Settings"}),
                rack_managers=({"name": "Rack Manager Name"}),
            ),
        )
