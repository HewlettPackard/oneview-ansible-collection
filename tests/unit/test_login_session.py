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

from mock import Mock, patch
import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import LoginSessionModule
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ONEVIEW_MODULE_UTILS_PATH
from hpeOneView.oneview_client import OneViewClient
from hpeOneView.connection import connection


ansible_fact = {"session": "testauth"}

MSG_CREATED = 'Session created successfully.'
MSG_NOT_CREATED = 'Session creation failed.'


PARAMS_FOR_PRESENT = dict(
    config='config.json',
    name='TestSession'
)


class TestLoginSessionModule:
    """
    TestCases for LoginSessionModule
    """

    def test_login_session(self):

        self.patcher_ansible = patch(ONEVIEW_MODULE_UTILS_PATH + '.AnsibleModule')
        self.patcher_ansible = self.patcher_ansible.start()
        ansible_module = Mock()
        self.patcher_ansible.return_value = ansible_module
        self.mock_ansible_module = ansible_module

        patcher_json_file = patch.object(OneViewClient, 'from_json_file')
        client = patcher_json_file.start()
        self.mock_ov_client = client.return_value
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT
        self.patcher_oneview_config = patch.object(LoginSessionModule, 'get_config').start()
        self.patcher_conn_obj = patch.object(connection, 'post').start()
        self.patcher_conn_obj.return_value = None, {'sessionID': 'testauth'}

        LoginSessionModule().run()

        self.mock_ansible_module.exit_json.assert_called_with(
            changed=True,
            msg=LoginSessionModule.MSG_CREATED,
            ansible_facts=ansible_fact
        )


if __name__ == '__main__':
    pytest.main([__file__])
