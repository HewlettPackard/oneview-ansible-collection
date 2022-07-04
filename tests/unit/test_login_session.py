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
from hpeOneView.connection import connection
import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import LoginSessionModule
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ONEVIEW_MODULE_UTILS_PATH
from hpeOneView.oneview_client import OneViewClient

a_fact = {"session" : "testauth"}

MSG_CREATED = 'Session created successfully.'
MSG_NOT_CREATED = 'Session creation failed.'

MODULE_EXECUTE_RETURN_VALUE = dict(
    changed=True,
    msg=MSG_CREATED,
    ansible_facts={'ansible_facts': None}
)

EXPECTED_ARG_SPEC = {'api_version': {'type': u'int'},
                        'config': {'type': 'path'},
                        'hostname': {'type': 'str'},
                        'image_streamer_hostname': {'type': 'str'},
                        'password': {'type': 'str', 'no_log': True},
                        'username': {'type': 'str'},
                        'auth_login_domain': {'type': 'str'},
                        'validate_etag': {'type': 'bool', 'default': True}}

PARAMS_FOR_PRESENT = dict(
    config = 'config.json',
    name = 'TestSession'
)

class TestLoginSessionModule:
    """
    TestCases for LoginSessionModule
    """

    patcher_ansible = patch(ONEVIEW_MODULE_UTILS_PATH + '.AnsibleModule')
    patcher_ansible = patcher_ansible.start()
    ansible_module = Mock()
    patcher_ansible.return_value = ansible_module
    mock_ansible_module = ansible_module

    def test_login_session(self):

        patcher_json_file = patch.object(OneViewClient, 'from_json_file')
        client = patcher_json_file.start()
        self.mock_ov_client = client.return_value
        self.mock_ansible_module.params = PARAMS_FOR_PRESENT
        self.patcher_oneview_config = patch.object(LoginSessionModule, 'get_config').start()
        self.patcher_conn_obj = patch.object(connection, 'post').start()
        self.patcher_conn_obj.return_value = None, {'sessionID':'testauth'}

        LoginSessionModule().run()

        self.mock_ansible_module.exit_json.assert_called_with(
            changed=True,
            msg=LoginSessionModule.MSG_CREATED,
            ansible_facts=a_fact
        )

        self.patcher_conn_obj.stop()
        self.patcher_oneview_config.stop()


if __name__ == '__main__':
    pytest.main([__file__])