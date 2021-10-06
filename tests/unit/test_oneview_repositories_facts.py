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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import RepositoriesFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Repositories"
)

REPOSITORY_1 = dict(name="Test Repository 1", uri='/rest/repositories/a0336853-58d7-e021-b740-511cf971e21f0')
REPOSITORY_2 = dict(name="Test Repository 2", uri='/rest/repositories/b3213123-44sd-y334-d111-asd34sdf34df3')

PRESENT_REPOSITORIES = [REPOSITORY_1, REPOSITORY_2]


@pytest.mark.resource(TestRepositoriesFactsModule='repositories')
class TestRepositoriesFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_repositories(self):
        self.resource.get_all.return_value = PRESENT_REPOSITORIES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        RepositoriesFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(repositories=PRESENT_REPOSITORIES)
        )

    def test_should_get_repositories_by_name(self):
        self.resource.data = REPOSITORY_2
        self.resource.get_by.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        RepositoriesFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(repositories=REPOSITORY_2)
        )


if __name__ == '__main__':
    pytest.main([__file__])
