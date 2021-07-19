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
      server: "16.85.88.10"
      port: 8080
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

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class ApplianceProxyConfigurationModule(OneViewModule):
    MSG_CREATED = 'Appliance Proxy Configured successfully.'
    MSG_UPDATED = 'Appliance Proxy updated successfully.'
    MSG_DELETED = 'Appliance Proxy deleted successfully.'
    MSG_ALREADY_PRESENT = 'Appliance Proxy Configuration is already present.'
    MSG_ALREADY_ABSENT = 'Appliance Proxy Configuration is already absent.'
    RESOURCE_FACT_NAME = 'appliance_proxy_configuration'

    def __init__(self):
        argument_spec = dict(
            data=dict(required=False, type='dict'),
            name=dict(required=False, type='str'),
            state=dict(
                required=True,
                choices=['present', 'absent']),
        )
        super().__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.appliance_proxy_configuration)

    def execute_module(self):
        if self.state == 'present':
            return self.resource_present(self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(self.RESOURCE_FACT_NAME)


def main():
    ApplianceProxyConfigurationModule().run()


if __name__ == '__main__':
    main()
