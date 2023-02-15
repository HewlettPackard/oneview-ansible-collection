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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_sas_logical_jbod
short_description: Manage OneView SAS Logical JBOD resources.
description:
    - Provides an interface to manage SAS Logical JBOD resources.
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
        - Indicates the desired patch operation for SAS logical JBOD
          C(present) will create a SAS logical JBOD.
          C(absent) will delete a SAS logical JBOD.
          C(change_name) will change the SAS logical JBOD name.
          C(change_description) will change the SAS logical jbod description.
          C(erase_data) will disable drive sanitize option.
          C(clear_metadata) will clear the meta data.
      choices: [
        'present', 'absent', 'change_name', 'change_description', 'erase_data', 'clear_metadata'
        ]
      type: str
      required: true
    validate_etag:
      description:
         - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag
           for the resource matches the ETag provided in the data.
      default: true
      choices: []
      type: bool
    data:
      description:
        - List with the SAS logical JBOD properties.
      required: true
      type: dict
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Create a SAS Logical JBOD
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: present
    data:
      name: "sas_logical_jbod_name"
      description: "Sas logical Jbod description"
      minSizeGB: 200
      maxSizeGB: 600
      numPhysicalDrives: 1
      driveTechnology:
        deviceInterface: "SAS"
        driveMedia: "HDD"
      driveEnclosureUris: "{{ drive_enclosure_uri_list }}"
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Create a SAS logical JBOD by providing specific drive bay URIs
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: present
    data:
      name: "{{ contents.sas_logical_jbod.sas_logical_jbod_name }}-1"
      description: "Sas logical Jbod description"
      eraseData: true
      driveBayUris: "{{ drive_bay_uris }}"
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Do nothing when JBOD already exists
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: present
    data:
      name: "sas_logical_jbod_name-1"
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Change name of an existing JBOD
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: change_name
    data:
      name: 'sas_logical_jbod_name'
      newName: 'sas_logical_jbod_name-renamed'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Do nothing when name is already the same
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: change_name
    data:
      name: 'sas_logical_jbod_name-renamed'
      newName: 'sas_logical_jbod_name-renamed'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Change description of an existing JBOD
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: change_description
    data:
      name: 'sas_logical_jbod_name-renamed'
      newDescription: 'New Description to JBOD'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Do nothing when description is already the same
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: change_description
    data:
      name: 'contents.sas_logical_jbod.sas_logical_jbod_name-renamed'
      newDescription: 'New Description to JBOD'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Disable drive sanitize option of an existing JBOD
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: erase_data
    data:
      name: 'sas_logical_jbod_name-renamed'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Do nothing when drive sanitize option is already disabled
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: erase_data
    data:
      name: 'sas_logical_jbod_name-renamed'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Clear metadata of an existing JBOD
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: clear_metadata
    data:
      name: 'sas_logical_jbod_name-renamed'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Delete an existing JBOD
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: absent
    data:
      name: 'sas_logical_jbod_name-renamed'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'

- name: Do nothing if JBOD is already deleted
  oneview_sas_logical_jbod:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: absent
    data:
      name: 'sas_logical_jbod_name-renamed'
  when: contents.sas_logical_jbod.variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: contents.sas_logical_jbod.variant == 'Synergy'
'''

RETURN = '''
sas_logical_jbod:
    description: Has all the facts about the SAS logical JBOD.
    returned: On states 'present', 'absent', 'change_name', 'change_description', 'erase_data', 'clear_metadata'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (OneViewModule, OneViewModuleResourceNotFound)


class SasLogicalJbodModule(OneViewModule):
    MSG_JBOD_CREATED = "SAS logical JBOD created successfully."
    MSG_JBOD_ALREADY_EXISTS = "SAS logical jbod with same name already exists."
    MSG_JBOD_NAME_CHANGED = "SAS logical JBOD name changed successfully."
    MSG_JBOD_NAME_NOT_CHANGED = "There is no change to existing SAS logical JBOD name."
    MSG_JBOD_DESCRIPTION_CHANGED = "SAS logical JBOD description changed successfully."
    MSG_JBOD_DESCRIPTION_NOT_CHANGED = "SAS logical JBOD description is already the same."
    MSG_DISABLED_DRIVE_SANITIZE_OPTION = "Disabled drive sanitize option successfully."
    MSG_DRIVE_SANITIZE_OPTION_ALREADY_DISABLED = "Drive sanitize option is already disabled."
    MSG_CLEARED_METADATA = "Cleared metadata successfully."
    MSG_METADATA_ALREADY_CLEARED = "Metadata is already cleared."
    MSG_JBOD_DELETED = "Deleted SAS logical JBOD successfully."
    MSG_JBOD_NOT_FOUND = "SAS logical JBOD not found."

    argument_spec = dict(
        state=dict(
            required=True,
            choices=[
                'present',
                'absent',
                'change_name',
                'change_description',
                'erase_data',
                'clear_metadata'
            ]
        ),
        sessionID=dict(required=False, type='str'),
        data=dict(required=True, type='dict')
    )

    patch_params = dict(
        change_name=dict(operation='replace', path='/name', value='sas_jbod_name'),
        change_description=dict(operation='replace', path='/description', value='sas_jbod_desc'),
        erase_data=dict(operation='replace', path='/eraseData', value='false'),
        clear_metadata=dict(operation='replace', path='/clearMetadata', value='true')
    )

    patch_messages = dict(
        change_name=dict(changed=MSG_JBOD_NAME_CHANGED, not_changed=MSG_JBOD_NAME_NOT_CHANGED),
        change_description=dict(changed=MSG_JBOD_DESCRIPTION_CHANGED, not_changed=MSG_JBOD_DESCRIPTION_NOT_CHANGED),
        erase_data=dict(changed=MSG_DISABLED_DRIVE_SANITIZE_OPTION, not_changed=MSG_DRIVE_SANITIZE_OPTION_ALREADY_DISABLED),
        clear_metadata=dict(changed=MSG_CLEARED_METADATA, not_changed=MSG_METADATA_ALREADY_CLEARED)
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.sas_logical_jbods)

    def execute_module(self):
        if self.state == "present":
            return self.__present()
        elif self.state == "absent":
            return self.resource_absent()
        else:
            if not self.current_resource:
                raise OneViewModuleResourceNotFound(self.MSG_JBOD_NOT_FOUND)
            else:
                changed, msg, resource = self.__patch(self.state)
        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(sas_logical_jbod=resource))

    def __present(self):
        if not self.current_resource:
            resource = self.resource_client.create(self.data)
            changed = True
            msg = self.MSG_JBOD_CREATED
        else:
            resource = self.current_resource
            changed = False
            msg = self.MSG_JBOD_ALREADY_EXISTS
        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(sas_logical_jbod=resource.data))

    def __patch(self, state):
        changed = False
        if "newName" in self.data:
            self.patch_params['change_name']['value'] = self.data.get("newName")
        elif "newDescription" in self.data:
            self.patch_params['change_description']['value'] = self.data.get("newDescription")
        state_name = self.module.params['state']
        state = self.patch_params[state_name].copy()

        current_property_value = self.__get_current_property_value(state_name, state)

        if self.__is_update_needed(state_name, state, current_property_value):
            resource_obj = self.current_resource.patch(**state)
            resource = resource_obj.data
            changed = True
        else:
            resource = self.current_resource.data

        msg = self.patch_messages[state_name]['changed'] if changed else self.patch_messages[state_name]['not_changed']

        return changed, msg, resource

    def __get_current_property_value(self, state_name, state):
        property_name = state['path'].split('/')[1]
        if self.current_resource.data.get(property_name) is not None:
            return self.current_resource.data.get(property_name)
        else:
            return None

    def __is_update_needed(self, state_name, state, current_property_value):
        need_request_update = False
        if state_name == "clearMetadata":
            need_request_update = True
        if str(current_property_value).lower() != state['value'].lower():
            need_request_update = True
        return need_request_update


def main():
    SasLogicalJbodModule().run()


if __name__ == '__main__':
    main()
