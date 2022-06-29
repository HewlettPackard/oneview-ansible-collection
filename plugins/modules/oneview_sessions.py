#!/usr/bin/python
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
import json

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''

Need to change the documentation
---
module: oneview_certificates_server
short_description: Manage OneView Server Certificate resources.
description:
    - Provides an interface to manage Server Certificate resources. Can create, update, and delete.
version_added: "2.4.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.4.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
        description:
            - Indicates the desired state for the Server Certificate resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
        type: str
    name:
        description:
            - Indicates the alias name of the certificates server resource.
        required: true
        type: str
    data:
        description:
            - List with the Server Certificate properties.
        required: true
        type: dict
extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Create a Server Certificate
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    name: "172.18.13.11"
    data:
      certificateDetails:
        - aliasName: 'vcenter'
          base64Data: '--- Certificate ---'
- name: Update the Server Certificate name to 'vcenter Renamed'
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    name: "172.18.13.11"
    data:
      name: 'vcenter renamed'
      certificateDetails:
        - aliasName: 'vcenter'
          base64Data: '--- Certificate ---'
- name: Ensure that the Hypervisor Manager is absent
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    name: "172.18.13.11"
    data:
      alias_name: 'vcenter'
'''

RETURN = '''
oneview_session:
    description: Has the facts about the oneview session created
    returned: On state 'present'.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule
from hpeOneView.oneview_client import OneViewClient
from hpeOneView.connection import connection

class SessionsManagement(OneViewModule):
    MSG_CREATED = 'Session created successfully.'

    def __init__(self):
        additional_arg_spec = dict(name=dict(required=True, type='str'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super().__init__(additional_arg_spec=additional_arg_spec,
                         validate_etag_support=True)

    def execute_module(self):

        with open(self.module.params['config']) as json_data:
            oneview_config = json.load(json_data)

        conn = connection(oneview_config.get('ip'), oneview_config.get('api_version'), oneview_config.get('ssl_certificate', False),
                                       oneview_config.get('timeout'))
        task, body = conn.post('/rest/login-sessions', oneview_config.get('credentials'))
        auth = body['sessionID']
        return dict(changed='True', msg=self.MSG_CREATED, ansible_facts={"session":auth})

def main():
    SessionsManagement().run()


if __name__ == '__main__':
    main()
