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

from mock import Mock, patch
import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import GetSessionIDModule
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ONEVIEW_MODULE_UTILS_PATH
from hpeOneView.oneview_client import OneViewClient
from hpeOneView.connection import connection


ansible_fact = {"session": "testauth"}

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    name='TestSession'
)


class TestLoginSessionModule:
    """
    TestCases for LoginSessionModule
    """
    def setup_method(self):
        self.patcher_ansible = patch(ONEVIEW_MODULE_UTILS_PATH + '.AnsibleModule')
        self.patcher_ansible = self.patcher_ansible.start()
        ansible_module = Mock()
        self.patcher_ansible.return_value = ansible_module
        self.mock_ansible_module = ansible_module

    @patch.object(OneViewClient, 'from_json_file')
    @patch.object(GetSessionIDModule, 'get_config')
    @patch.object(connection, 'post')
    def test_login_session(self, mock_post, mock_get_config, mock_from_json_file):
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT
        mock_from_json_file.return_value.connection.get_session_id.return_value = 'testauth'

        GetSessionIDModule().run()

        self.mock_ansible_module.exit_json.assert_called_with(
            changed=True,
            msg=GetSessionIDModule.MSG_CREATED,
            ansible_facts=ansible_fact
        )

    @patch.object(OneViewClient, 'from_json_file')
    @patch.object(GetSessionIDModule, 'get_config')
    @patch.object(connection, 'post')
    def test_login_session_without_config(self, mock_post, mock_get_config, mock_from_json_file):
        mock_get_config.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT
        mock_post.return_value = None, {'sessionID': 'testauth'}

        GetSessionIDModule().run()

        self.mock_ansible_module.exit_json.assert_called_with(
            changed=False,
            msg=GetSessionIDModule.MSG_NOT_CREATED,
            ansible_facts=None
        )


if __name__ == '__main__':
    pytest.main([__file__])
