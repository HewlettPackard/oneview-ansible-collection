# -*- coding: utf-8 -*-
###
# Copyright (2022) Hewlett Packard Enterprise Development LP
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
module: oneview_rack_manager
short_description: Manage OneView Rack Manager resources.
description:
    - "Provides an interface to manage Server Hardware resources."
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Alisha Kalladassery (@alisha-k-kalladassery)"
options:
    sessionID:
        description:
            - Session ID to use for login to the appliance
        type: str
        required: false
    state:
        description:
            - Indicates the desired state for the Rack manager resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(refresh_state_set) will refresh the Rack manager.
        choices: ['present', 'absent', 'refresh_state_set']
        required: true
        type: str
    data:
        description:
            - List with Server Hardware properties and its associated states.
        required: true
        type: dict

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.validateetag
'''

EXAMPLES = '''
- name: Add a Rack Manager
  oneview_rack_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: present
    data:
      hostname: "5.6.7.8"
      username: "username"
      password: "password"
      force: false
  delegate_to: localhost

- name: Gather facts about all Rack Managers
  oneview_rack_manager_facts:
    hostname: 5.6.7.8
    username: administrator
    password: my_password
    api_version: 4400
  delegate_to: localhost

- debug: var=rack_managers
- set_fact:
    rack_manager_name: "{{ rack_managers[0]['name'] }}"

- name: Do nothing when the rack manager is already present
  oneview_rack_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: present
    data:
      hostname: "{{ rack_manager_name }}"
      username: 'username'
      password: 'password'
      force: false
  delegate_to: localhost

- name: Refresh the rack manager
  oneview_rack_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: refresh_state_set
    data:
      name: "{{ rack_manager_name }}"
  delegate_to: localhost

- name: Remove the rack manager by its name
  oneview_rack_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: absent
    data:
      name: "{{ rack_manager_name }}"
  delegate_to: localhost

- name: Do nothing when the rack manager is already removed
  oneview_rack_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: absent
    data:
      name: "{{ rack_manager_name }}"
  delegate_to: localhost
'''

RETURN = '''
rack_manager:
    description: Has the OneView facts about the Rack Manager.
    returned: On states 'present', 'power_state_set', 'refresh_state_set'.
              Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (OneViewModule, OneViewModuleResourceNotFound,
                                                                          OneViewModuleValueError)


class RackManagerModule(OneViewModule):
    MSG_ADDED = 'Rack Manager added successfully.'
    MSG_ALREADY_PRESENT = 'Rack Manager is already present.'
    MSG_DELETED = 'Rack Manager deleted successfully.'
    MSG_ALREADY_ABSENT = 'Rack Manager is already absent.'
    MSG_RACK_MANAGER_REFRESHED = 'Rack Manager refreshed successfully.'
    MSG_RACK_MANAGER_NOT_FOUND = 'The provided rack manager was not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=[
                'present',
                'absent',
                'refresh_state_set'
            ]
        ),
        sessionID=dict(required=False, type='str'),
        data=dict(required=True, type='dict')
    )

    def __init__(self):

        super().__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.rack_managers)

    def execute_module(self):

        result = {}
        if self.state == 'present':
            result = self.__present()
        else:
            if not self.data.get('name'):
                raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.name"))

            if self.state == 'absent':
                result = self.resource_absent(method='remove')
            else:
                if not self.current_resource:
                    raise OneViewModuleResourceNotFound(self.MSG_RACK_MANAGER_NOT_FOUND)
                else:
                    if self.state == 'refresh_state_set':
                        self.current_resource.patch('RefreshRackManagerOp', '', '')
                        result = dict(changed=True,
                                      msg=self.MSG_RACK_MANAGER_REFRESHED,
                                      ansible_facts=dict(rack_manager=self.current_resource.data))
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        if result:
            return result

    def __present(self):

        if not self.data.get('hostname'):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.hostname"))

        self.current_resource = self.resource_client.get_by_name(self.data['hostname'])

        result = dict()

        if not self.current_resource:
            self.current_resource = self.resource_client.add(self.data)
            result = dict(
                changed=True,
                msg=self.MSG_ADDED,
                ansible_facts={'rack_manager': self.current_resource.data}
            )
        else:
            result = dict(
                changed=False,
                msg=self.MSG_ALREADY_PRESENT,
                ansible_facts={'rack_manager': self.current_resource.data}
            )
        return result


def main():
    RackManagerModule().run()


if __name__ == '__main__':
    main()
