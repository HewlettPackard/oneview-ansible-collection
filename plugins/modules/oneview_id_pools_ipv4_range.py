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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_id_pools_ipv4_range
short_description: Manage OneView ID pools IPV4 Range resources.
description:
    - Provides an interface to manage ID pools IPV4 Range resources. Can create, update, or delete.
version_added: "2.5.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 6.0.0"
    - "ansible >= 2.9"
author: "Thiago Miotto (@tmiotto)"
options:
    state:
        description:
            - Indicates the desired state for the ID pools IPV4 Range resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        type: str
        required: true
    data:
        description:
            - List with ID pools IPV4 Range properties.
        type: dict
        required: true

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that ID pools IPV4 Range is present using the default configuration
  oneview_id_pools_ipv4_range:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test ID pools IPV4 Range'

- name: Ensure that ID pools IPV4 Range is absent
  oneview_id_pools_ipv4_range:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'ID pools IPV4 Range'
'''

RETURN = '''
id_pools_ipv4_range:
    description: Has the facts about the OneView ID pools IPV4 Ranges.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class IdPoolsIpv4RangeModule(OneViewModule):
    MSG_CREATED = 'ID pools IPV4 Range created successfully.'
    MSG_UPDATED = 'ID pools IPV4 Range updated successfully.'
    MSG_DELETED = 'ID pools IPV4 Range deleted successfully.'
    MSG_ALREADY_PRESENT = 'ID pools IPV4 Range is already present.'
    MSG_ALREADY_ABSENT = 'ID pools IPV4 Range is already absent.'
    RESOURCE_FACT_NAME = 'id_pools_ipv4_range'

    def __init__(self):

        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super().__init__(additional_arg_spec=additional_arg_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.id_pools_ipv4_ranges

    def execute_module(self):
        self.current_resource = None
        # If Range URI is provided then it sets the resource client
        if self.data.get('uri'):
            self.current_resource = self.resource_client.get_by_uri(self.data.get('uri'))
        # Do preliminary check before creating a new range
        elif self.data.get('subnetUri') and self.data.get('name'):
            subnet = self.oneview_client.id_pools_ipv4_subnets.get_by_uri(self.data.get('subnetUri'))
            for range_uri in subnet.data['rangeUris']:
                maybe_resource = self.resource_client.get_by_uri(range_uri)
                if maybe_resource.data['name'] == self.data['name']:
                    self.current_resource = maybe_resource

        if self.state == 'present':
            return self._present()
        elif self.state == 'absent':
            return self.resource_absent()

    def _present(self):
        # If no resource was found during get operation, it creates new one
        if not self.current_resource:
            response = self.resource_present("id_pools_ipv4_range")
        else:
            # setting current resource for _update_resource
            # Enabled can be True, False or None. Using not found default to false for comparison purposes.
            enabled = self.data.pop('enabled', 'not_given')
            # sets update_collector/update_allocator if Given to True.
            update_collector = self.data.pop('update_collector', False)
            update_allocator = self.data.pop('update_allocator', False)
            id_list = self.data.pop('idList', False)
            count = self.data.pop('count', False)
            # In case newName is given it sets it correctly
            if self.data.get('newName'):
                self.data['name'] = self.data.pop('newName')
            # It Performs the update operation
            response = self.resource_present("id_pools_ipv4_range")
            # Checks enabled status in latest data and performas accordingly
            if enabled != 'not_given' and enabled != self.current_resource.data.get('enabled'):
                response['msg'] = self.MSG_UPDATED
                response['changed'] = True
                response['ansible_facts']['id_pools_ipv4_range'] = \
                    self.resource_client.enable(dict(enabled=enabled, type='Range'), self.current_resource.data['uri'])
                self.data['enabled'] = enabled
                return response
            elif update_collector:
                response['msg'] = self.MSG_UPDATED
                response['changed'] = True
                self.data['idList'] = id_list
                response['ansible_facts']['id_pools_ipv4_range'] = \
                    self.resource_client.update_collector(dict(idList=id_list), self.data.get('uri'))
                return response
            elif update_allocator:
                self.data['idList'] = id_list
                self.data['count'] = count
                response['msg'] = self.MSG_UPDATED
                response['changed'] = True
                response['ansible_facts']['id_pools_ipv4_range'] = \
                    self.resource_client.update_allocator(dict(idList=id_list, count=count), self.data.get('uri'))
        return response


def main():
    IdPoolsIpv4RangeModule().run()


if __name__ == '__main__':
    main()
