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
module: oneview_appliance_network_interfaces
short_description: Manage the Appliance Network Interfaces.
description:
    - Provides an interface to manage the Appliance Network Interfaces.
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
    state:
        description:
          - Indicates the desired state for the Appliance Network Interface.
            C(present) ensures data properties are compliant with OneView.
        choices: ['present']
        type: str
        required: true
    data:
        description:
            - List with the Network Interface.
        required: true
        type: dict

extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Creates Network Interface
  oneview_appliance_network_interfaces:
    config: "{{ config }}"
    state: present
    data:
      interfaceName: "Appliance test"
      device: "eth0"
      macAddress: "{{mac_address}}"
      ipv4Type: "STATIC"
      ipv6Type: "UNCONFIGURE"
      hostname: "{{hostname}}"
      app1Ipv4Addr: "{{app1_ipv4_address}}"
      app2Ipv4Addr: "{{app2_ipv4_address}}"
      virtIpv4Addr: "{{ ipv4_address }}"
      ipv4Subnet: "{{ ipv4_subnet }}"
      ipv4Gateway: "{{ gateway }}"
      ipv4NameServers:
        - "{{ dnsServer1 }}"
        - "{{ dnsServer2 }}"
  delegate_to: localhost
- debug: var=appliance_network_interfaces
'''

RETURN = '''
appliance_network_interface:
    description: Has all the OneView facts about the OneView appliance network interface.
    returned: On state 'present'.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, dict_merge, compare


class ApplianceNetworkInterfacesModule(OneViewModule):
    MSG_CREATED = 'Appliance Network Interface created successfully.'
    MSG_ALREADY_PRESENT = 'Appliance Proxy Configuration is already present.'

    def __init__(self):
        argument_spec = dict(
            sessionID=dict(required=False, type='str'),
            data=dict(required=True, type='dict'),
            state=dict(
                required=True,
                choices=['present']),
        )
        super().__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.appliance_network_interfaces

    def execute_module(self):
        result = {}
        self.current_resource = self.resource_client.get_by_mac_address(self.data.get('macAddress'))
        if self.state == 'present':
            result = self.__present()
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        return result

    def __present(self):
        changed, field_changed, data = False, False, {}
        if self.current_resource:
            existing_data = self.current_resource.data.copy()
            updated_data = dict_merge(existing_data, self.data)

            if not compare(self.current_resource.data, updated_data):
                field_changed = True
                self.data = updated_data

        if not self.current_resource or field_changed:
            data["applianceNetworks"] = [self.data]
            self.current_resource = self.resource_client.create(data)
            changed, msg = True, self.MSG_CREATED
        else:
            msg = self.MSG_ALREADY_PRESENT
        return dict(
            msg=msg,
            changed=changed,
            ansible_facts=dict(appliance_network_interfaces=self.current_resource.data)
        )


def main():
    ApplianceNetworkInterfacesModule().run()


if __name__ == '__main__':
    main()
