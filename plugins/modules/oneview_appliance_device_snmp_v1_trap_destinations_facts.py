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
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_appliance_device_snmp_v1_trap_destinations_facts
short_description: Retrieve the facts about the OneView appliance SNMPv1 trap forwarding destinations.
description:
    - The appliance has the ability to forward events received from monitored or managed server hardware
       to the specified destinations as SNMPv1 traps.
       This module retrives the facts about the appliance SNMPv1 trap forwarding destinations.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author:
    "Venkatesh Ravula (@VenkateshRavula)"
options:
    name:
      description:
        -  destination address of snmpv1 trap.
      required: false
      type: str
    uri:
      description:
        - snmpv1 trap uri.
      required: false
      type: str
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(sort): The sort order of the returned data set.
          C(query): A general query string to narrow the list of resources returned."
      required: false
      type: dict
extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.factsparams
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about all appliance SNMPv1 trap forwarding destinations.
  oneview_appliance_device_snmp_v1_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v1_trap_destinations

- name: Gather paginated, filtered and sorted facts about SNMPv1 trap forwarding destinations
  oneview_appliance_device_snmp_v1_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    params:
      start: 0
      count: 3
      sort: 'destination:descending'
      filter: "port='162'"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v1_trap_destinations

- name: Gather facts about a Trap Destination by Destination
  oneview_appliance_device_snmp_v1_trap_destinations_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    name: '1.1.1.1'
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v1_trap_destinations
'''

RETURN = '''
appliance_device_snmp_v1_trap_destinations:
    description: Has all the OneView facts about the OneView appliance SNMPv1 trap forwarding destinations.
    returned: Always.
    type: dict
'''


from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class ApplianceDeviceSnmpV1TrapDestinationsFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        uri=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.appliance_device_snmp_v1_trap_destinations)

    def execute_module(self):
        appliance_device_snmp_v1_trap_destinations = []

        if self.current_resource:
            appliance_device_snmp_v1_trap_destinations = self.current_resource.data
        elif not self.module.params.get('name') or self.module.params.get('uri'):
            appliance_device_snmp_v1_trap_destinations = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(appliance_device_snmp_v1_trap_destinations=appliance_device_snmp_v1_trap_destinations))


def main():
    ApplianceDeviceSnmpV1TrapDestinationsFactsModule().run()


if __name__ == '__main__':
    main()
