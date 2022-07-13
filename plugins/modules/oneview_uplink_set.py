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
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_uplink_set
short_description: Manage OneView Uplink Set resources.
version_added: "2.3.0"
description:
    - Provides an interface to manage Uplink Set resources. Can create, update, or delete.
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Uplink Set resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              The key used to find the resource to perform the operation is a compound key, that consists of
              the name of the uplink set and the URI (or name) of the Logical Interconnect combined. You can choose to
              set the Logical Interconnect by logicalInterconnectUri or logicalInterconnectName.
        choices: ['present', 'absent']
        type: str
        required: true
    data:
        description:
            - List with Uplink Set properties.
        required: true
        type: dict
notes:
    - "To rename an uplink set you must inform a C(newName) in the data argument. The rename is non-idempotent"

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the Uplink Set is present
  oneview_uplink_set:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: present
    data:
      name: 'Test Uplink Set'
      status: "OK"
      # You can choose set the Logical Interconnect by logicalInterconnectUri or logicalInterconnectName
      logicalInterconnectName: "Name of the Logical Interconnect"                                   # option 1
      # logicalInterconnectUri: "/rest/logical-interconnects/461a9cef-beef-4916-8be1-926078ffb948"  # option 2
      networkUris: [
         '/rest/ethernet-networks/9e8472ad-5ad1-4cbd-aab1-566b67ffc6a4',
         '/rest/ethernet-networks/28ea7c1a-4930-4432-854b-30cf239226a2'
      ]
      fcNetworkUris: []
      fcoeNetworkUris: []
      portConfigInfos: []
      connectionMode: "Auto"
      networkType: "Ethernet"
      manualLoginRedistributionState: "NotSupported"

- name: Rename the Uplink Set from 'Test Uplink Set' to 'Renamed Uplink Set'
  oneview_uplink_set:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: present
    data:
      name: 'Test Uplink Set'
      newName: 'Renamed Uplink Set'
      logicalInterconnectName: "Name of the Logical Interconnect"

- name: Ensure that the Uplink Set is absent
  oneview_uplink_set:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: absent
    data:
      name: 'Test Uplink Set'
      logicalInterconnectName: "Name of the Logical Interconnect"
'''

RETURN = '''
uplink_set:
    description: Has the OneView facts about the Uplink Set.
    returned: On state 'present'. Can be null.
    type: dict
'''
from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, OneViewModuleValueError


class UplinkSetModule(OneViewModule):
    MSG_KEY_REQUIRED = "Uplink Set Name and Logical Interconnect required."
    MSG_CREATED = 'Uplink Set created successfully.'
    MSG_UPDATED = 'Uplink Set updated successfully.'
    MSG_DELETED = 'Uplink Set deleted successfully.'
    MSG_ALREADY_PRESENT = 'Uplink Set is already present.'
    MSG_ALREADY_ABSENT = 'Uplink Set is already absent.'
    MSG_LOGICAL_INTERCONNECT_NOT_FOUND = "Logical Interconnect not found."
    MSG_NETWORK_NOT_FOUND = "Network not found."
    RESOURCE_FACT_NAME = 'uplink_set'

    def __init__(self):
        argument_spec = dict(
            state=dict(required=True, choices=['present', 'absent']),
            data=dict(required=True, type='dict')
        )
        super().__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.uplink_sets)

    def execute_module(self):
        self.__validate_key()
        self.__replace_logical_interconnect_name_by_uri()
        self.__replace_network_name_by_uri()

        self.__set_current_resource(self.data['name'], self.data['logicalInterconnectUri'])

        if self.state == 'present':
            return self.resource_present(self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent()

    def __validate_key(self):
        if 'name' not in self.data:
            raise OneViewModuleValueError(self.MSG_KEY_REQUIRED)
        if 'logicalInterconnectUri' not in self.data and 'logicalInterconnectName' not in self.data:
            raise OneViewModuleValueError(self.MSG_KEY_REQUIRED)

    def __replace_logical_interconnect_name_by_uri(self):
        if 'logicalInterconnectName' in self.data:
            name = self.data.pop('logicalInterconnectName')
            logical_interconnect = self.oneview_client.logical_interconnects.get_by_name(name)
            if logical_interconnect:
                self.data['logicalInterconnectUri'] = logical_interconnect.data['uri']
            else:
                raise OneViewModuleResourceNotFound(self.MSG_LOGICAL_INTERCONNECT_NOT_FOUND)

    def __get_ethernet_network_by_name(self, record):
        if record and record.startswith('/rest/'):
            return record
        else:
            result = self.oneview_client.ethernet_networks.get_by_name(record)
            if result:
                return result.data['uri']
            else:
                raise OneViewModuleResourceNotFound(self.MSG_NETWORK_NOT_FOUND + record)

    def __get_fc_network_by_name(self, record):
        if record and record.startswith('/rest/'):
            return record
        else:
            result = self.oneview_client.fc_networks.get_by_name(record)
            if result:
                return result.data['uri']
            else:
                raise OneViewModuleResourceNotFound(self.MSG_NETWORK_NOT_FOUND + record)

    def __get_fcoe_network_by_name(self, record):
        if record and record.startswith('/rest/'):
            return record
        else:
            result = self.oneview_client.fcoe_networks.get_by_name(record)
            if result:
                return result.data['uri']
            else:
                raise OneViewModuleResourceNotFound(self.MSG_NETWORK_NOT_FOUND + record)

    def __replace_network_name_by_uri(self):
        if 'networkUris' in self.data and self.data['networkUris']:
            self.data['networkUris'] = [self.__get_ethernet_network_by_name(record) for record in self.data['networkUris']]
        if 'fcNetworkUris' in self.data and self.data['fcNetworkUris']:
            self.data['fcNetworkUris'] = [self.__get_fc_network_by_name(record) for record in self.data['fcNetworkUris']]
        if 'fcoeNetworkUris' in self.data and self.data['fcoeNetworkUris']:
            self.data['fcoeNetworkUris'] = [self.__get_fcoe_network_by_name(record) for record in self.data['fcoeNetworkUris']]

    def __set_current_resource(self, name, logical_interconnect_uri):
        uplink_sets = self.resource_client.get_by('name', name)
        uplink_sets = [x for x in uplink_sets if x['logicalInterconnectUri'] == logical_interconnect_uri]
        if uplink_sets:
            self.current_resource = self.resource_client.get_by_uri(uplink_sets[0]["uri"])


def main():
    UplinkSetModule().run()


if __name__ == '__main__':
    main()
