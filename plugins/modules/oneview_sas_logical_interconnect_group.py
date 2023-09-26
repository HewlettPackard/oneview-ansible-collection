#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2023) Hewlett Packard Enterprise Development LP
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
module: oneview_sas_logical_interconnect_group
short_description: Manage OneView SAS Logical Interconnect Group resources.
description:
    - Provides an interface to manage SAS Logical Interconnect Group resources. Can create, update, or delete.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Alisha K (@alisha-k-kalladassery)"
options:
    sessionID:
        description:
            - Session ID to use for login to the appliance
        type: str
        required: false
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
            - List with the SAS Logical Interconnect Group properties.
        required: true
        type: dict
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.validateetag
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Fetch Session Id
  oneview_get_session_id:
    config: "{{ config }}"
    name: "Test_Session"
  delegate_to: localhost
  register: session

- debug: var=session

- name: Create a SAS Logical Interconnect Group
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: present
    data:
      name: '{{ item.name }}'
      enclosureType: 'SY12000'
      interconnectBaySet: 1
      enclosureIndexes: [1]
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - enclosureIndex: 1
            logicalLocation:
                locationEntries:
                    - relativeValue: 1
                      type: "Enclosure"
                    - relativeValue: 4
                      type: "Bay"
            permittedInterconnectTypeName: "{{ contents.sas_logical_interconnect_group.permitted_interconnect_type_name }}"
          - enclosureIndex: 1
            logicalLocation:
                locationEntries:
                    - relativeValue: 1
                      type: "Enclosure"
                    - relativeValue: 1
                      type: "Bay"
            permittedInterconnectTypeName: "{{ contents.sas_logical_interconnect_group.permitted_interconnect_type_name }}"
            # Alternatively you can inform permittedInterconnectTypeUri
  delegate_to: localhost
  with_items:
    - { name: 'SAS LIG' }
    - { name: 'SAS Test Logical Interconnect Group' }

- name: Do nothing with the Logical Interconnect Group when no changes are provided
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: present
    data:
      name: 'SAS Test Logical Interconnect Group'
      enclosureType: 'SY12000'
  delegate_to: localhost

- name: Rename the Logical Interconnect Group to 'Updated SAS Logical Interconnect Group'
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: present
    data:
      name: 'SAS Test Logical Interconnect Group'
      newName: 'Updated SAS Logical Interconnect Group'
  delegate_to: localhost

- name: Delete the Logical Interconnect Group
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: absent
    data:
      name: 'Updated SAS Logical Interconnect Group'
  delegate_to: localhost
  register: deleted

- name: Do nothing when the Logical Interconnect Group is absent
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: absent
    data:
      name: 'Updated Logical Interconnect Group'
  delegate_to: localhost
  register: deleted
'''

RETURN = '''
sas_logical_interconnect_group:
    description: Has the facts about the OneView SAS Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound


class SasLogicalInterconnectGroupModule(OneViewModule):
    MSG_CREATED = 'SAS Logical Interconnect Group created successfully.'
    MSG_UPDATED = 'SAS Logical Interconnect Group updated successfully.'
    MSG_DELETED = 'SAS Logical Interconnect Group deleted successfully.'
    MSG_ALREADY_PRESENT = 'SAS Logical Interconnect Group is already present.'
    MSG_ALREADY_ABSENT = 'SAS Logical Interconnect Group is already absent.'
    MSG_SAS_INTERCONNECT_TYPE_NOT_FOUND = 'SAS Interconnect Type was not found.'

    RESOURCE_FACT_NAME = 'sas_logical_interconnect_group'

    def __init__(self):
        argument_spec = dict(
            sessionID=dict(required=False, type='str'),
            state=dict(required=True, choices=['present', 'absent']),
            data=dict(required=True, type='dict')
        )

        super().__init__(additional_arg_spec=argument_spec,
                         validate_etag_support=True)
        self.set_resource_object(self.oneview_client.sas_logical_interconnect_groups)

    def execute_module(self):
        result = {}
        if self.state == 'present':
            result = self.__present()
        elif self.state == 'absent':
            result = self.resource_absent()
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        return result

    def __present(self):
        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")
        self.__replace_name_by_uris()

        result = self.resource_present(self.RESOURCE_FACT_NAME)

        return result

    def __replace_name_by_uris(self):
        map_template = self.data.get('interconnectMapTemplate')
        if map_template:
            map_entry_templates = map_template.get('interconnectMapEntryTemplates')
            if map_entry_templates:
                for value in map_entry_templates:
                    permitted_interconnect_type_name = value.pop('permittedInterconnectTypeName', None)
                    if permitted_interconnect_type_name:
                        value['permittedInterconnectTypeUri'] = self.__get_interconnect_type_by_name(
                            permitted_interconnect_type_name)

    def __get_interconnect_type_by_name(self, name):
        i_type = self.oneview_client.sas_interconnect_types.get_by_name(name)
        if i_type:
            return i_type.data['uri']
        else:
            raise OneViewModuleResourceNotFound(self.MSG_SAS_INTERCONNECT_TYPE_NOT_FOUND)


def main():
    SasLogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
