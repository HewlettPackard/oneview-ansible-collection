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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_network_set
short_description: Manage OneView Network Set resources.
description:
    - Provides an interface to manage Network Set resources. Can create, update, or delete.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
      description:
        - Indicates the desired state for the Network Set resource.
          C(present) ensures data properties are compliant with OneView.
          C(absent) removes the resource from OneView, if it exists.
      choices: ['present', 'absent']
      type: str
      required: true
    data:
      description:
        - List with the Network Set properties.
      required: true
      type: dict
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Network Set
  oneview_network_set:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      networkUris:
        - 'Test Ethernet Network_1'                                       # can be a name
        - '/rest/ethernet-networks/e4360c9d-051d-4931-b2aa-7de846450dd8'  # or a URI

- name: Update the Network Set name to 'OneViewSDK Test Network Set - Renamed' and change the associated networks
  oneview_network_set:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      newName: 'OneViewSDK Test Network Set - Renamed'
      networkUris:
        - 'Test Ethernet Network_1'

- name: Delete the Network Set
  oneview_network_set:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: absent
    data:
        name: 'OneViewSDK Test Network Set - Renamed'

# This feature is only available for V300 and V500
- name: Update the Network set with two scopes
  oneview_network_set:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    data:
      name: OneViewSDK Test Network Set
      scopeUris:
        - /rest/scopes/01SC123456
        - /rest/scopes/02SC123456
  delegate_to: localhost
'''

RETURN = '''
network_set:
    description: Has the facts about the Network Set.
    returned: On state 'present', but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, compare


class NetworkSetModule(OneViewModule):
    MSG_CREATED = 'Network Set created successfully.'
    MSG_UPDATED = 'Network Set updated successfully.'
    MSG_DELETED = 'Network Set deleted successfully.'
    MSG_ALREADY_PRESENT = 'Network Set is already present.'
    MSG_ALREADY_ABSENT = 'Network Set is already absent.'
    MSG_ETHERNET_NETWORK_NOT_FOUND = 'Ethernet Network not found: '
    MSG_CONNECTION_TEMPLATE_NOT_FOUND = 'Connection Template not found.'
    RESOURCE_FACT_NAME = 'network_set'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict'))

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.network_sets)
        self.connection_templates = self.oneview_client.connection_templates

    def execute_module(self):

        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.resource_absent()

    def __present(self):

        bandwidth = self.data.pop('bandwidth', None)
        scope_uris = self.data.pop('scopeUris', None)
        self.__replace_network_name_by_uri(self.data)
        result = self.resource_present(self.RESOURCE_FACT_NAME)

        if bandwidth:
            changed, connection_template = self.__update_connection_template(bandwidth)
            if changed:
                result['changed'] = changed
                result['msg'] = self.MSG_UPDATED
                result['ansible_facts'][self.RESOURCE_FACT_NAME]['connection_template'] = connection_template
            else:
                result['changed'] = changed
                result['msg'] = self.MSG_ALREADY_PRESENT

        if scope_uris is not None:
            result = self.resource_scopes_set(result, self.RESOURCE_FACT_NAME, scope_uris)
        return result

    def __get_ethernet_network_by_name(self, name):

        result = self.oneview_client.ethernet_networks.get_by('name', name)
        return result[0] if result else None

    def __get_network_uri(self, network_name_or_uri):

        if network_name_or_uri and network_name_or_uri.startswith('/rest/ethernet-networks'):
            return network_name_or_uri
        else:
            enet_network = self.__get_ethernet_network_by_name(network_name_or_uri)
            if enet_network:
                return enet_network['uri']
            else:
                raise OneViewModuleResourceNotFound(self.MSG_ETHERNET_NETWORK_NOT_FOUND + network_name_or_uri)

    def __replace_network_name_by_uri(self, data):

        if 'networkUris' in data:
            data['networkUris'] = [self.__get_network_uri(x) for x in data['networkUris']]
        if 'nativeNetworkUri' in data and data['nativeNetworkUri']:
            data['nativeNetworkUri'] = self.__get_network_uri(data['nativeNetworkUri'])

    # Update network set connection template with bandwidth
    def __update_connection_template(self, bandwidth):
        if 'connectionTemplateUri' not in self.current_resource.data:
            raise OneViewModuleResourceNotFound(self.MSG_CONNECTION_TEMPLATE_NOT_FOUND)

        connection_template = self.connection_templates.get_by_uri(
            self.current_resource.data['connectionTemplateUri'])

        merged_data = connection_template.data.copy()
        merged_data.update({'bandwidth': bandwidth})

        if not compare(connection_template.data, merged_data):
            connection_template.update(merged_data)
            return True, connection_template.data
        else:
            return False, connection_template.data


def main():
    NetworkSetModule().run()


if __name__ == '__main__':
    main()
