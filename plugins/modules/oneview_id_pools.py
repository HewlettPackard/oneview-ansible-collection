#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021-2024, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

__metaclass__ = type

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_id_pools
short_description: Manage OneView Id Pools.
description:
    - Provides an interface to manage Id pools. Can retrieve, update.
version_added: "2.4.0"
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
            - Indicates the desired state for the ID Pools resource.
              C(update_pool_type_ will enable or disable the pool
              C(allocate) will allocate set of ID's from IPv4 Subnet.
              C(collect) will collect the allocated ID's.
              C(validate) will verify ids are valid or not.
        choices: ['update_pool_type', 'allocate', 'collect', 'validate']
        required: true
        type: str
    data:
        description:
            - dict with required params.
        required: true
        type: dict
extends_documentation_fragment:
  - hpe.oneview.oneview
  - hpe.oneview.oneview.validateetag
  - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Enables or disables the pool type
  oneview_id_pools:
    config: "{{ config }}"
    state: update_pool_type
    data:
      poolType: '{{ poolType }}'
      rangeUris: '{{ id_pool["rangeUris"] }}'
      enabled: true
  delegate_to: localhost

- name: Allocates one or more IDs from a pool
  oneview_id_pools:
    config: "{{ config }}"
    state: allocate
    data:
      poolType: '{{ poolType }}'
      count: 2
  delegate_to: localhost

- name: Validates a set of IDs to reserve in the pool
  oneview_id_pools:
    config: "{{ config }}"
    state: validate
    data:
      poolType: '{{ poolType }}'
      idList: '{{ id_pool["idList"] }}'
  delegate_to: localhost

- name: Collects one or more IDs to be returned to a pool
  oneview_id_pools:
    config: "{{ config }}"
    state: collect
    data:
      poolType: '{{ poolType }}'
      rangeUris: '{{ id_pool["idList"] }}'
  delegate_to: localhost
'''

RETURN = '''
id_pool:
    description: Has the facts about the Id Pools.
    returned: On all states
    type: dict

'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, OneViewModuleValueError


class IdPoolsModule(OneViewModule):
    MSG_UPDATED = 'Pool updated successfully.'
    MSG_ALLOCATED = 'IDs have been reserved.'
    MSG_COLLECTED = 'Allocated IDs have been collected.'
    MSG_VALIDATED = 'Pool IDs are valid'
    MSG_ALREADY_PRESENT = 'Pool Updated already.'
    MSG_IDS_NOT_AVAILABLE = 'Ids not available'
    RESOURCE_FACT_NAME = 'id_pools'

    argument_spec = dict(
        sessionID=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['allocate', 'collect', 'validate', 'update_pool_type']
        ),
        data=dict(required=True, type='dict'),
    )

    def __init__(self):

        super().__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)

        self.set_resource_object(self.oneview_client.id_pools)

    def execute_module(self):

        changed, msg, id_pool = False, '', {}

        poolType = self.data.pop('poolType', '')
        idList = self.data.pop('idList', [])
        count = self.data.pop('count', 0)

        if self.state == 'update_pool_type':
            changed, msg, id_pool = self.__update_pool_type(poolType)
        elif self.state == 'allocate':
            changed, msg, id_pool = self.__allocate({'count': count}, poolType)
        elif self.state == 'collect':
            changed, msg, id_pool = self.__collect({'idList': idList}, poolType)
        elif self.state == 'validate':
            changed, msg, id_pool = self.__validate({'idList': idList}, poolType)

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=changed, msg=msg, ansible_facts=dict(id_pool=id_pool))

    def __update_pool_type(self, poolType):
        updated_pool = self.resource_client.update_pool_type(self.data, poolType)

        if self.data['enabled'] != updated_pool['enabled']:
            return True, self.MSG_UPDATED, updated_pool
        else:
            return False, self.MSG_ALREADY_PRESENT, updated_pool

    def __collect(self, idList, poolType):
        collect = self.resource_client.collect(idList, poolType)

        if collect['idList']:
            return True, self.MSG_COLLECTED, collect
        else:
            return False, self.MSG_IDS_NOT_AVAILABLE, collect

    def __allocate(self, count, poolType):
        try:
            allocate = self.resource_client.allocate(count, poolType)
            return True, self.MSG_ALLOCATED, allocate

        except OneViewModuleValueError:
            raise OneViewModuleValueError(self.MSG_IDS_NOT_AVAILABLE)

    def __validate(self, idDict, poolType):
        validate = self.resource_client.validate(idDict, poolType)

        if validate['idList']:
            return True, self.MSG_VALIDATED, validate
        else:
            return False, self.MSG_IDS_NOT_AVAILABLE, validate


def main():
    IdPoolsModule().run()


if __name__ == '__main__':
    main()
