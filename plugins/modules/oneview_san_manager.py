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
module: oneview_san_manager
short_description: Manage OneView san Manager resources.
description:
    - "Provides an interface to manage San Manager resources."
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Nabhajit Ray (@NabhajitRay)"
options:
    sessionID:
        description:
            - Session ID to use for login to the appliance
        type: str
        required: false
    state:
        description:
            - Indicates the desired state for the san manager resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
              C(refresh_state_set) will refresh the san manager.
        choices: ['present', 'absent', 'refresh_state_set']
        required: true
        type: str
    data:
        description:
            - List with San Managers and its associated states.
        required: true
        type: dict
notes:
    - If you need to update password of san manager, you should pass "updatePassword" field as true as in
      example given below. In all other cases, password won't be considered while updating the san manager.

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.validateetag
'''

EXAMPLES = '''
- name: Add a san Manager
  oneview_san_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: present
    data:
      providerDisplayName: "<san_manager_provider_display_name>"
      connectionInfo:
        - name: "Host"
          value: "<san_manager_hostname>"
        - name: "Username"
          value: "<san_manager_username>"
        - name: "Password"
          value: "<san_manager_password>"
        - name: "UseHttps"
          value: true
  delegate_to: localhost

- name: Gather facts about all san Managers
  oneview_san_manager_facts:
    hostname: 5.6.7.8
    username: administrator
    password: my_password
    api_version: 4600
  delegate_to: localhost
- debug: var=san_managers
- set_fact:
    san_manager_name: "{{ san_managers[0]['name'] }}"

- name: Do nothing when the san manager is already present
  oneview_san_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: present
    data:
      providerDisplayName: "<san_manager_provider_display_name>"
      connectionInfo:
        - name: "Host"
          value: "<san_manager_hostname>"
        - name: "Username"
          value: "<san_manager_username>"
        - name: "Password"
          value: "<san_manager_password>"
        - name: "UseHttps"
          value: true
  delegate_to: localhost

- name: Refresh the san manager
  oneview_san_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: refresh_state_set
    data:
      name: "{{ san_manager_name }}"
      refreshState: "RefreshPending"
  delegate_to: localhost

- name: Update the San Manager
  oneview_san_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: present
    data:
      name: "{{ san_manager_name }}"
      connectionInfo:
        - name: "Host"
          value: "<san_manager_hostname>"
        - name: "Username"
          value: "<san_manager_username>"
        - name: "Password"
          value: "<san_manager_password>"
        - name: "UseHttps"
          value: true
  delegate_to: localhost

- name: Update password of San Manager
  oneview_san_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4400
    state: present
    data:
      name: "{{ san_manager_name }}"
      connectionInfo:
        - name: "Host"
          value: "<san_manager_hostname>"
        - name: "Username"
          value: "<san_manager_username>"
        - name: "Password"
          value: "<san_manager_password>"
          updatePassword: true
        - name: "UseHttps"
          value: true
  delegate_to: localhost

- name: Remove the san manager by its name
  oneview_san_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: absent
    data:
      name: "{{ san_manager_name }}"
  delegate_to: localhost

- name: Do nothing when the san manager is already removed
  oneview_san_manager:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    state: absent
    data:
      name: "{{ san_manager_name }}"
  delegate_to: localhost
'''

RETURN = '''
san_manager:
    description: Has the OneView facts about the san Manager.
    returned: On states 'present', 'power_state_set', 'refresh_state_set'.
              Can be null.
    type: dict
'''
from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (OneViewModule, OneViewModuleResourceNotFound,
                                                                          OneViewModuleValueError, compare)
from operator import itemgetter
import copy


class SanManagerModule(OneViewModule):
    MSG_ADDED = 'san Manager added successfully.'
    MSG_ALREADY_PRESENT = 'San Manager is already present.'
    MSG_DELETED = 'san Manager deleted successfully.'
    MSG_ALREADY_ABSENT = 'San Manager is already absent.'
    MSG_PROVIDER_NOT_FOUND = 'The provided Provider was not found.'
    MSG_SAN_MANAGER_REFRESHED = 'San Manager refreshed successfully.'
    MSG_SAN_MANAGER_NOT_FOUND = 'The provided san manager was not found.'
    MSG_SAN_MANAGER_UPDATED = 'San Manager updated successfully.'

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
        self.set_resource_object(self.oneview_client.san_managers)
        self.san_providers = self.oneview_client.san_providers

    def execute_module(self):
        result = {}
        if self.state == 'present':
            if self.data.get('name'):
                self.current_resource = self.resource_client.get_by_name(self.data['name'])
                if self.current_resource:
                    result = self.__update()
                else:
                    result = self.__present()
            else:
                result = self.__present()
        else:
            if self.state == 'absent':
                result = self.resource_absent(method='remove')
            else:
                if self.data.get('name'):
                    self.current_resource = self.resource_client.get_by_name(self.data['name'])
                if not self.current_resource:
                    raise OneViewModuleResourceNotFound(self.MSG_SAN_MANAGER_NOT_FOUND)
                else:
                    if self.state == 'refresh_state_set':
                        info = {
                            'refreshState': self.data['refreshState']
                        }
                        self.current_resource.update(info, self.current_resource.data.get('uri'))
                        result = dict(changed=False,
                                      msg=self.MSG_SAN_MANAGER_REFRESHED,
                                      ansible_facts=dict(san_managers=self.current_resource.data))
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        if result:
            return result

    def __present(self):
        if not self.data.get('connectionInfo'):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.connectionInfo"))
        if not self.data.get('providerDisplayName'):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.providerDisplayName"))

        self.current_resource = self.resource_client.get_by_name(self.data.get('name'))

        result = dict()

        if not self.current_resource:
            if self.san_providers.get_provider_uri(self.data.get('providerDisplayName')) is None:
                raise OneViewModuleResourceNotFound(self.MSG_PROVIDER_NOT_FOUND)
            else:
                provider_uri = self.san_providers.get_provider_uri(self.data['providerDisplayName'])
                self.current_resource = self.san_providers.add(self.data, provider_uri)
                result = dict(
                    changed=True,
                    msg=self.MSG_ADDED,
                    ansible_facts={'san_managers': self.current_resource}
                )
        else:
            result = dict(
                changed=False,
                msg=self.MSG_ALREADY_PRESENT,
                ansible_facts={'san_managers': self.current_resource.data}
            )
        return result

    # Function to merge connectionInfo list in san manager
    def merge_data(self, connection1, connection2):
        connection1 = sorted(connection1, key=itemgetter('name'))
        connection2 = sorted(connection2, key=itemgetter('name'))
        for (i, j) in zip(connection1, connection2):
            i.update(j)
        return connection1

    def __update(self):
        connectionInfo = self.data.get("connectionInfo")
        update_password = False
        parameter_to_ignore = None
        for ele in connectionInfo:
            if ele.get("name") == "Password":
                if "updatePassword" in ele:
                    update_password = ele.get("updatePassword")
                    ele.pop("updatePassword")
                    if (update_password is True or update_password == "true"):
                        update_password = True
                    else:
                        update_password = False
        if not update_password:
            parameter_to_ignore = {"name": "Password"}
        merged_data = copy.deepcopy(self.current_resource.data)
        # Merging connectionInfo list to avoid data overwrite
        merged_connection_data = self.merge_data(merged_data['connectionInfo'], self.data['connectionInfo'])
        data = self.data
        data['connectionInfo'] = merged_connection_data
        merged_data.update(data)
        if not compare(self.current_resource.data, merged_data, parameter_to_ignore=parameter_to_ignore):
            self.current_resource.update(merged_data, self.current_resource.data.get('uri'))
            return dict(changed=True,
                        msg=self.MSG_SAN_MANAGER_UPDATED,
                        ansible_facts=dict(san_managers=self.current_resource.data))
        else:
            return dict(changed=False, msg=self.MSG_ALREADY_PRESENT, ansible_facts=dict(san_managers=self.current_resource.data))


def main():
    SanManagerModule().run()


if __name__ == '__main__':
    main()
