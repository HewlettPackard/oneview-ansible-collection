#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import RepositoriesModule

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_REPOSITORY_TEMPLATE = dict(
    name='New Repository',
    userName='username',
    password='password',
    repositoryURI='uri',
    repositoryType='FirmwareExternalRepo'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_REPOSITORY_TEMPLATE['name'])
)

PARAMS_FOR_PATCH = dict(
    config='config.json',
    state='patch',
    data=dict(name=DEFAULT_REPOSITORY_TEMPLATE['name'],
              newName='New Name')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_REPOSITORY_TEMPLATE['name'])
)


@pytest.mark.resource(TestRepositoriesModule='repositories')
class TestRepositoriesModule(OneViewBaseTest):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def test_should_create_new_repository(self):
        self.resource.get_by_name.return_value = []
        self.resource.create.return_value = self.resource
        self.resource.data = DEFAULT_REPOSITORY_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        RepositoriesModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RepositoriesModule.MSG_CREATED,
            ansible_facts=dict(repository=DEFAULT_REPOSITORY_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.data = DEFAULT_REPOSITORY_TEMPLATE
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT.copy()

        RepositoriesModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RepositoriesModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(repository=DEFAULT_REPOSITORY_TEMPLATE)
        )

    def test_update_repositoryName(self):
        params_to_scope = PARAMS_FOR_PATCH.copy()
        self.mock_ansible_module.params = params_to_scope

        self.resource.get_by_name.return_value = self.resource

        patch_return = self.resource.data
        obj = mock.Mock()
        obj.data = patch_return
        self.resource.patch.return_value = obj

        RepositoriesModule().run()

        self.resource.patch.assert_called_once_with(operation='replace',
                                                    path='/repositoryName',
                                                    value='New Name')

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(repository=patch_return),
            msg=RepositoriesModule.MSG_UPDATED
        )

    def test_should_remove_repository(self):
        self.resource.data = DEFAULT_REPOSITORY_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        RepositoriesModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=RepositoriesModule.MSG_DELETED,
            ansible_facts=dict(repository=None)
        )

    def test_should_do_nothing_when_repository_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        RepositoriesModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=RepositoriesModule.MSG_ALREADY_ABSENT,
            ansible_facts=dict(repository=None)
        )


if __name__ == '__main__':
    pytest.main([__file__])
