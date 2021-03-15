#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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
module: oneview_logical_interconnect_group
short_description: Manage OneView Logical Interconnect Group resources.
description:
    - Provides an interface to manage Logical Interconnect Group resources. Can create, update, or delete.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Interconnect Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
        type: str
    data:
        description:
            - List with the Logical Interconnect Group properties.
        required: true
        type: dict
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.validateetag
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Ensure that the Logical Interconnect Group is present
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      uplinkSets: []
      enclosureType: 'C7000'
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalDownlinkUri: ~
            logicalLocation:
                locationEntries:
                    - relativeValue: "1"
                      type: "Bay"
                    - relativeValue: 1
                      type: "Enclosure"
            permittedInterconnectTypeName: 'HP VC Flex-10/10D Module'
            # Alternatively you can inform permittedInterconnectTypeUri

# Below Task is available only till OneView 3.10
- name: Ensure that the Logical Interconnect Group has the specified scopes
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      scopeUris:
        - '/rest/scopes/00SC123456'
        - '/rest/scopes/01SC123456'

- name: Ensure that the Logical Interconnect Group is present with uplinkSets
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: present
    data:
      name: 'Test Logical Interconnect Group'
      uplinkSets:
        - name: 'e23 uplink set'
          mode: 'Auto'
          networkType: 'Ethernet'
          networkNames:
            - 'TestNetwork_1'
          networkUris:
            - '/rest/ethernet-networks/b2be27ec-ae31-41cb-9f92-ff6da5905abc'
          logicalPortConfigInfos:
            - desiredSpeed: 'Auto'
              logicalLocation:
                  locationEntries:
                    - relativeValue: 1
                      type: "Bay"
                    - relativeValue: 23
                      type: "Port"
                    - relativeValue: 1
                      type: "Enclosure"

- name: Ensure that the Logical Interconnect Group is present with name 'Test'
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: present
    data:
      name: 'New Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the Logical Interconnect Group is absent
  oneview_logical_interconnect_group:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    state: absent
    data:
      name: 'New Logical Interconnect Group'
'''

RETURN = '''
logical_interconnect_group:
    description: Has the facts about the OneView Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound


class LogicalInterconnectGroupModule(OneViewModule):
    MSG_CREATED = 'Logical Interconnect Group created successfully.'
    MSG_UPDATED = 'Logical Interconnect Group updated successfully.'
    MSG_DELETED = 'Logical Interconnect Group deleted successfully.'
    MSG_ALREADY_PRESENT = 'Logical Interconnect Group is already present.'
    MSG_ALREADY_ABSENT = 'Logical Interconnect Group is already absent.'
    MSG_INTERCONNECT_TYPE_NOT_FOUND = 'Interconnect Type was not found.'
    MSG_ETHERNET_NETWORK_NOT_FOUND = 'Ethernet Network was not found.'

    RESOURCE_FACT_NAME = 'logical_interconnect_group'

    def __init__(self):
        argument_spec = dict(
            state=dict(required=True, choices=['present', 'absent']),
            data=dict(required=True, type='dict')
        )

        super().__init__(additional_arg_spec=argument_spec,
                         validate_etag_support=True)
        self.set_resource_object(self.oneview_client.logical_interconnect_groups)

    def execute_module(self):
        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.resource_absent()

    def __present(self):
        scope_uris = self.data.pop('scopeUris', None)

        self.__replace_name_by_uris()
        self.__uplink_set_update()
        result = self.resource_present(self.RESOURCE_FACT_NAME)

        if scope_uris is not None:
            result = self.resource_scopes_set(result, 'logical_interconnect_group', scope_uris)

        return result

    def __replace_name_by_uris(self):
        # replace internalNetworkNames with internalNetworkUris
        internalNetworkUris = self.data.get('internalNetworkUris', [])
        internalNetworkNames = self.data.pop('internalNetworkNames', None)
        if internalNetworkNames:
            int_networkUris = [self.__get_network_uri(x) for x in internalNetworkNames]
            internalNetworkUris.extend(int_networkUris)
        self.data['internalNetworkUris'] = internalNetworkUris

        map_template = self.data.get('interconnectMapTemplate')
        if map_template:
            map_entry_templates = map_template.get('interconnectMapEntryTemplates')
            if map_entry_templates:
                for value in map_entry_templates:
                    permitted_interconnect_type_name = value.pop('permittedInterconnectTypeName', None)
                    if permitted_interconnect_type_name:
                        value['permittedInterconnectTypeUri'] = self.__get_interconnect_type_by_name(
                            permitted_interconnect_type_name).get('uri')

    def __uplink_set_update(self):
        if 'uplinkSets' in self.data:
            if self.__get_all_uplink_sets():
                allUplinkSets = self.__get_all_uplink_sets()
                for uplinkSet in self.data['uplinkSets']:
                    networkNames = uplinkSet.pop('networkNames', None)
                    if networkNames and not uplinkSet.get('networkUris'):
                        uplinkSet['networkUris'] = []
                    if networkNames:
                        networkUris = [self.__get_network_uri(x) for x in networkNames]
                        uplinkSet['networkUris'].extend(networkUris)
                    allUplinkSets = self.__update_existing_uplink_set(allUplinkSets, uplinkSet)
                self.data['uplinkSets'] = allUplinkSets
            else:
                self.__update_network_uri()

    def __update_network_uri(self):
        for i in range(len(self.data['uplinkSets'])):
            networkNames = self.data['uplinkSets'][i].pop('networkNames', None)
            if networkNames and not self.data['uplinkSets'][i].get('networkUris'):
                self.data['uplinkSets'][i]['networkUris'] = []
            if networkNames:
                networkUris = [self.__get_network_uri(x) for x in networkNames]
                self.data['uplinkSets'][i]['networkUris'].extend(networkUris)

    def __update_existing_uplink_set(self, allUplinkSets, newUplinkSet):
        temp = True
        for i, ups in enumerate(allUplinkSets):
            if ups['name'] == newUplinkSet['name']:
                temp = False
                if 'networkUris' in newUplinkSet:
                    newUris = set(newUplinkSet['networkUris']) - set(ups['networkUris'])
                    if newUris:
                        ups['networkUris'].extend(newUris)
                if 'networkSetUris' in newUplinkSet:
                    newUris = set(newUplinkSet['networkSetUris']) - set(ups['networkSetUris'])
                    if newUris:
                        ups['networkSetUris'].extend(newUris)
                allUplinkSets[i] = ups
        if temp:
            allUplinkSets.append(newUplinkSet)
        return allUplinkSets

    def __get_all_uplink_sets(self):
        lig_uri = self.oneview_client.logical_interconnect_groups.get_by('name', self.data['name'])
        if lig_uri:
            return lig_uri[0]['uplinkSets']
        return False

    def __get_network_uri(self, name):
        network_name = self.oneview_client.ethernet_networks.get_by('name', name)
        if network_name:
            return network_name[0]['uri']
        return False

    def __get_interconnect_type_by_name(self, name):
        i_type = self.oneview_client.interconnect_types.get_by('name', name)
        if i_type:
            return i_type[0]
        else:
            raise OneViewModuleResourceNotFound(self.MSG_INTERCONNECT_TYPE_NOT_FOUND)


def main():
    LogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
