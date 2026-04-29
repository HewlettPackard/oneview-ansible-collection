#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021-2024, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_id_pools_ipv4_subnet
short_description: Manage OneView ID pools IPV4 Subnet resources.
description:
    - Provides an interface to manage ID pools IPV4 Subnet resources. Can create, update, or delete.
version_added: "2.5.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author: "Yuvarani Chidambaram(@yuvirani)"
options:
    sessionID:
        description:
          - Session ID to use for login to the appliance
        type: str
        required: false
    state:
        description:
            - Indicates the desired state for the ID pools IPV4 Subnet resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(allocate) will allocate set of ID's from IPv4 subnet
              C(collect) will collect the allocated IDs'
        choices: ['present', 'absent', 'allocate', 'collect']
        required: true
        type: str
    data:
        description:
            - List with ID pools IPV4 Subnet properties.
        required: true
        type: dict

extends_documentation_fragment:
  - hpe.oneview.oneview
  - hpe.oneview.oneview.validateetag
  - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Ensure that ID pools IPV4 Subnet is present using the default configuration
  oneview_id_pools_ipv4_subnet:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test ID pools IPV4 Subnet'
      vlanId: '201'

- name: Ensure that ID pools IPV4 Subnet is absent
  oneview_id_pools_ipv4_subnet:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'ID pools IPV4 Subnet'
'''

RETURN = '''
id_pools_ipv4_subnet:
    description: Has the facts about the OneView ID pools IPV4 Subnets.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class IdPoolsIpv4SubnetModule(OneViewModule):
    MSG_CREATED = 'ID pools IPV4 Subnet created successfully.'
    MSG_UPDATED = 'ID pools IPV4 Subnet updated successfully.'
    MSG_DELETED = 'ID pools IPV4 Subnet deleted successfully.'
    MSG_ALLOCATE = 'IDs found and have been allocated'
    MSG_NO_ALLOCATE = 'No ids found for allocation'
    MSG_COLLECT = 'Collected the ids allocated'
    RESOURCE_FACT_NAME = 'id_pools_ipv4_subnet'

    additional_arg_spec = dict(sessionID=dict(required=False, type='str'),
                               data=dict(required=True, type='dict'),
                               state=dict(required=True,
                               choices=['present', 'absent', 'allocate', 'collect']))

    def __init__(self):

        super().__init__(additional_arg_spec=self.additional_arg_spec, validate_etag_support=True)

        self.resource_client = self.oneview_client.id_pools_ipv4_subnets

    def execute_module(self):
        changed, msg, ipv4_subnet = False, '', {}
        result = {}

        if self.data.get('networkId', ''):
            self.current_resource = self.resource_client.get_by_field('networkId', self.data.get('networkId'))
        elif self.data.get('uri', ''):
            self.current_resource = self.resource_client.get_by_uri(self.data.get('uri'))

        if self.state == 'present':
            result = self.resource_present(self.RESOURCE_FACT_NAME)
        elif self.state == 'allocate':
            changed, msg, ipv4_subnet = self.__allocator(self.current_resource)
            result = dict(changed=changed, msg=msg, ansible_facts=dict(id_pools_ipv4_subnet=ipv4_subnet))
        elif self.state == 'collect':
            changed, msg, ipv4_subnet = self.__collector(self.current_resource)
            result = dict(changed=changed, msg=msg, ansible_facts=dict(id_pools_ipv4_subnet=ipv4_subnet))
        elif self.state == 'absent':
            result = self.resource_absent()

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        if result:
            return result

    def __allocator(self, resource):
        subnet_id = resource.data['allocatorUri'].split('/')[-2]
        allocate = self.resource_client.allocate({'count': self.data['count']}, subnet_id)
        return True, self.MSG_ALLOCATE, allocate

    def __collector(self, resource):
        subnet_id = resource.data['allocatorUri'].split('/')[-2]
        collect = self.resource_client.collect({'idList': self.data['idList']}, subnet_id)
        return True, self.MSG_COLLECT, collect


def main():
    IdPoolsIpv4SubnetModule().run()


if __name__ == '__main__':
    main()
