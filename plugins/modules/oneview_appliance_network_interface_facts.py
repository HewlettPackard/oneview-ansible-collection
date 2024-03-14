#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021-2024) Hewlett Packard Enterprise Development LP
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
module: oneview_appliance_network_interface_facts
short_description: Retrieve the facts about the OneView appliance network interfaces.
description:
    - Retrieve the facts about the OneView appliance network interfaces.
version_added: "2.9.0"
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
    params:
        description:
          - mac_address of the Appliance Network Interface.
        type: dict
        required: false
    options:
      description:
        - "List with options to gather additional facts about unconfigured mac addresses.
           Options allowed:
           C(getAllMacAddress)."
      required: false
      type: list
      elements: str
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about the Appliance Network Interface
  oneview_appliance_network_interface_facts:
    config: "{{ config }}"
  delegate_to: localhost

- name: Gather facts about the Network Interfaces by Mac Address
  oneview_appliance_network_interface_facts:
    config: "{{ config }}"
    params:
      mac_address: "{{ mac_address }}"
  delegate_to: localhost

- name: Gather facts about the all unconfigured Mac Addresses
  oneview_appliance_network_interface_facts:
    config: "{{ config }}"
    options:
      - getAllMacAddress
  delegate_to: localhost

- debug: var=appliance_network_interfaces
'''

RETURN = '''
appliance_network_interfaces:
    description: Has all the OneView facts about the Appliance network interfaces.
    returned: Always.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class ApplianceNetworkInterfaceFactsModule(OneViewModule):
    argument_spec = dict(
        sessionID=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
        options=dict(required=False, type='list', elements='str')
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, supports_check_mode=True)
        self.set_resource_object(self.oneview_client.appliance_network_interfaces)

    def execute_module(self):

        if self.module.params.get('mac_address'):
            network_interfaces = self.resource_client.get_by_mac_address(self.module.params.get('mac_address')).data
        elif 'getAllMacAddress' in self.options:
            network_interfaces = self.resource_client.get_all_mac_address()
        else:
            network_interfaces = self.resource_client.get_all().data

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False,
                    ansible_facts=dict(appliance_network_interfaces=network_interfaces))


def main():
    ApplianceNetworkInterfaceFactsModule().run()


if __name__ == '__main__':
    main()
