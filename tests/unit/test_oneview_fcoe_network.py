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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import FcoeNetworkModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_FCOE_NETWORK_TEMPLATE = dict(
    name='New FCoE Network 2',
    vlanId="201",
    connectionTemplateUri=None
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FCOE_NETWORK_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FCOE_NETWORK_TEMPLATE['name'],
              fabricType='DirectAttach',
              newName='New Name')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_FCOE_NETWORK_TEMPLATE['name'])
)


@pytest.mark.resource(TestFcoeNetworkModule='fcoe_networks')
class TestFcoeNetworkModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_fcoe_network(self):
        self.resource.get_by_name.return_value = []
        self.resource.create.return_value = self.resource
        self.resource.data = DEFAULT_FCOE_NETWORK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcoeNetworkModule.MSG_CREATED,
            ansible_facts=dict(fcoe_network=DEFAULT_FCOE_NETWORK_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_FCOE_NETWORK_TEMPLATE
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT.copy()

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcoeNetworkModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(fcoe_network=DEFAULT_FCOE_NETWORK_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_FCOE_NETWORK_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.data = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcoeNetworkModule.MSG_UPDATED,
            ansible_facts=dict(fcoe_network=data_merged)
        )

    def test_should_remove_fcoe_network(self):
        self.resource.data = DEFAULT_FCOE_NETWORK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcoeNetworkModule.MSG_DELETED
        )

    def test_should_do_nothing_when_fcoe_network_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcoeNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcoeNetworkModule.MSG_ALREADY_ABSENT
        )

    def test_update_scopes_when_different(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_FCOE_NETWORK_TEMPLATE.copy()
        resource_data['scopeUris'] = ['fake']
        resource_data['uri'] = 'rest/fcoe/fake'
        self.resource.data = resource_data

        patch_return = resource_data.copy()
        patch_return['scopeUris'] = ['test']
        patch_return_obj = self.resource.copy()
        patch_return_obj.data = patch_return
        self.resource.patch.return_value = patch_return_obj

        FcoeNetworkModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/scopeUris',
                                                    value=['test'])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(fcoe_network=patch_return),
            msg=FcoeNetworkModule.MSG_UPDATED
        )

    def test_should_do_nothing_when_scopes_are_the_same(self):
        params_to_scope = PARAMS_FOR_PRESENT.copy()
        params_to_scope['data']['scopeUris'] = ['test']
        self.mock_ansible_module.params = params_to_scope

        resource_data = DEFAULT_FCOE_NETWORK_TEMPLATE.copy()
        resource_data['scopeUris'] = ['test']
        self.resource.data = resource_data

        FcoeNetworkModule().run()

        self.resource.patch.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fcoe_network=resource_data),
            msg=FcoeNetworkModule.MSG_ALREADY_PRESENT
        )

    def test_should_delete_bulk_fcoe_networks(self):
        networkUris = [
            "/rest/fcoe-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548",
            "/rest/fcoe-networks/f2f0031b-52bd-4223-9ac1-d91cb519d549",
            "/rest/fcoe-networks/02f0031b-52bd-4223-9ac1-d91cb519d54a"
        ]

        PARAMS_FOR_BULK_DELETED = dict(
            config='config.json',
            state='absent',
            data=dict(networkUris=[
                "/rest/fcoe-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548",
                "/rest/fcoe-networks/f2f0031b-52bd-4223-9ac1-d91cb519d549",
                "/rest/fcoe-networks/02f0031b-52bd-4223-9ac1-d91cb519d54a"
            ])
        )

        self.resource.delete_bulk.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_BULK_DELETED

        FcoeNetworkModule().run()

        self.resource.delete_bulk.assert_called_once_with({'networkUris': networkUris})
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True, msg=FcoeNetworkModule.MSG_BULK_DELETED,
            ansible_facts=dict(fcoe_network_bulk_delete=None))


if __name__ == '__main__':
    pytest.main([__file__])
