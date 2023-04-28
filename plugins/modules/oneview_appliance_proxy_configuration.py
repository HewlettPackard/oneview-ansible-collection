#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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
ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_appliance_proxy_configuration
short_description: Manage the Appliance Proxy Configuration.
description:
    - Provides an interface to manage the Appliance Proxy Config.
version_added: "2.5.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.3.0"
author:
    "Yuvarani Chidambaram (@yuvirani)"
options:
    sessionID:
        description:
            - Session ID to use for login to the appliance
        type: str
        required: false
    logout:
        description:
            - Param to logout from the appliance when the task is done.
        type: bool
        required: false
    state:
        description:
          - Indicates the desired state for the Appliance Proxy Config.
            C(present) ensures data properties are compliant with OneView.
            C(absent) removes the resource from OneView, if it exists.
        choices: ['present', 'absent']
        type: str
        required: true
    data:
        description:
            - List with the Proxy Config.
        required: false
        type: dict

extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Creates Proxy with HTTP protocol
  oneview_appliance_proxy_configuration:
    config: "{{ config }}"
    state: present
    data:
      server: "<server_ip>"
      port: 443
      username: "proxydcs"
      password: "dcs"
      communicationProtocol: "HTTP"
  delegate_to: localhost
- debug: var=appliance_proxy_configuration

- name: Deletes the configured proxy
  oneview_appliance_proxy_configuration:
    config: "{{ config }}"
    state: present
  delegate_to: localhost
'''

RETURN = '''
appliance_proxy_configuration:
    description: Has all the OneView facts about the OneView appliance proxy config.
    returned: On state 'present' and 'absent'.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, dict_merge, compare


class ApplianceProxyConfigurationModule(OneViewModule):
    MSG_CREATED = 'Appliance Proxy Configured successfully.'
    MSG_ALREADY_PRESENT = 'Appliance Proxy Configuration is already present.'

    def __init__(self):
        argument_spec = dict(
            sessionID=dict(required=False, type='str'),
            logout=dict(required=False, type='bool'),
            data=dict(required=False, type='dict'),
            state=dict(
                required=True,
                choices=['present', 'absent']),
        )
        super().__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.appliance_proxy_configuration

    def execute_module(self):
        self.current_resource = self.resource_client.get_by_proxy(self.data.get('server'))
        if self.state == 'present':
            result = self.__present()
        elif self.state == 'absent':
            result = self.__absent()
        if self.module.params.get('logout'):
            self.oneview_client.connection.logout()
        return result

    def __present(self):
        changed, field_changed = False, False
        # password field always null for existing resource
        # ignored for comparison
        if self.current_resource:
            user_data = self.data.copy()
            if user_data.get('password'):
                user_data.pop('password')
            existing_data = self.current_resource.data.copy()
            if existing_data.get('password'):
                existing_data.pop('password')
            updated_data = dict_merge(existing_data, user_data)
            if not compare(existing_data, updated_data):
                field_changed = True

        if not self.current_resource or field_changed:
            self.current_resource = self.resource_client.create(self.data)
            changed, msg = True, self.MSG_CREATED
        else:
            msg = self.MSG_ALREADY_PRESENT
        return dict(
            msg=msg,
            changed=changed,
            ansible_facts=dict(appliance_proxy_configuration=self.current_resource.data)
        )

    def __absent(self):
        changed = False
        if self.current_resource:
            self.resource_client.delete()
            changed, msg = True, self.MSG_DELETED
        else:
            msg = self.MSG_ALREADY_ABSENT
        return dict(
            msg=msg,
            changed=changed,
        )


def main():
    ApplianceProxyConfigurationModule().run()


if __name__ == '__main__':
    main()
