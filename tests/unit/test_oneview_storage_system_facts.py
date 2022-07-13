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

import pytest
import mock

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import StorageSystemFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Storage Systems"
)

PARAMS_GET_BY_IP_HOSTNAME = dict(
    config='config.json',
    storage_hostname='172.0.0.0'
)

PARAMS_GET_BY_HOSTNAME = dict(
    config='config.json',
    storage_hostname='172.0.0.0'
)

PARAMS_GET_HOST_TYPES = dict(
    config='config.json',
    options=["hostTypes"]
)

PARAMS_GET_REACHABLE_PORTS = dict(
    config='config.json',
    storage_hostname='172.0.0.0',
    options=["reachablePorts"]
)

PARAMS_GET_TEMPLATES = dict(
    config='config.json',
    storage_hostname='172.0.0.0',
    options=["templates"]
)

HOST_TYPES = [
    "Citrix Xen Server 5.x/6.x",
    "IBM VIO Server",
]

PARAMS_GET_POOL_BY_NAME = dict(
    config='config.json',
    name="Test Storage Systems",
    options=["storagePools"]
)

PARAMS_GET_POOL_BY_IP_HOSTNAME = dict(
    config='config.json',
    storage_hostname='172.0.0.0',
    options=["storagePools"]
)


@pytest.mark.resource(TestStorageSystemFactsModule='storage_systems')
class TestStorageSystemFactsModule(OneViewBaseFactsTest):
    @pytest.fixture(autouse=True)
    def specific_set_up(self, setUp):
        self.mock_ov_client.api_version = 300

    def test_should_get_all_storage_system(self):
        self.resource.get_all.return_value = {"name": "Storage System Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_systems=({"name": "Storage System Name"}))
        )

    def test_should_get_storage_system_by_name(self):
        self.resource.data = {"name": "Storage System Name"}
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_systems=([{"name": "Storage System Name"}]))
        )

    def test_should_get_storage_system_by_ip_hostname(self):
        self.resource.data = {"ip_hostname": "172.0.0.0"}
        self.resource.get_by_ip_hostname.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_HOSTNAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_systems=([{"ip_hostname": "172.0.0.0"}]))
        )

    def test_should_get_storage_system_by_hostname(self):
        self.mock_ov_client.api_version = 500
        self.resource.data = {"hostname": "172.0.0.0"}
        self.resource.get_by_hostname.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_HOSTNAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_systems=([{"hostname": "172.0.0.0"}]))
        )

    def test_should_get_all_host_types(self):
        self.resource.get_host_types.return_value = HOST_TYPES
        self.resource.get_all.return_value = [{"name": "Storage System Name"}]
        self.mock_ansible_module.params = PARAMS_GET_HOST_TYPES

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_host_types=HOST_TYPES,
                storage_systems=[{"name": "Storage System Name"}])
        )

    def test_should_get_reachable_ports(self):
        self.mock_ov_client.api_version = 500
        self.resource.get_reachable_ports.return_value = [{'port': 'port1'}]

        self.resource.data = {"name": "Storage System Name", "uri": "rest/123"}
        self.resource.get_by_hostname.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_GET_REACHABLE_PORTS

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_reachable_ports=[{'port': 'port1'}],
                storage_systems=[{"name": "Storage System Name", "uri": "rest/123"}])
        )

    def test_should_get_templates(self):
        self.mock_ov_client.api_version = 500
        self.resource.get_templates.return_value = [{'template': 'temp'}]

        self.resource.data = {"name": "Storage System Name", "uri": "rest/123"}
        self.resource.get_by_hostname.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_TEMPLATES

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_templates=[{'template': 'temp'}],
                storage_systems=[{"name": "Storage System Name", "uri": "rest/123"}]
            )
        )

    def test_should_get_storage_pools_system_by_name(self):
        self.resource.data = {"name": "Storage System Name", "uri": "uri"}
        self.resource.get_by_name.return_value = self.resource
        self.resource.get_storage_pools.return_value = {"name": "Storage Pool"}
        self.mock_ansible_module.params = PARAMS_GET_POOL_BY_NAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_pools=({"name": "Storage Pool"}),
                storage_systems=[{"name": "Storage System Name", "uri": "uri"}]
            )
        )

    def test_should_get_storage_system_pools_by_ip_hostname(self):
        self.resource.data = {"ip_hostname": "172.0.0.0", "uri": "uri"}

        self.resource.get_by_ip_hostname.return_value = self.resource
        self.resource.get_storage_pools.return_value = {"name": "Storage Pool"}

        self.mock_ansible_module.params = PARAMS_GET_POOL_BY_IP_HOSTNAME

        StorageSystemFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                storage_system_pools=({"name": "Storage Pool"}),
                storage_systems=[{"ip_hostname": "172.0.0.0", "uri": "uri"}]
            )
        )


if __name__ == '__main__':
    pytest.main([__file__])
