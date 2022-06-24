#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
module: oneview_repositories
short_description: Manage OneView Repository resources.
description:
    - Provides an interface to manage repositories. Can create, update, or delete repositories, and modify the repository membership by
      adding or removing resource assignments.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Chebrolu Harika (@ChebroluHarika)"
options:
    state:
        description:
            - Indicates the desired state for the repository resource.
              C(present) ensures data properties are compliant with OneView.
              C(absent) removes the resource from OneView, if it exists.
              C(patch) modifies repository membership by updating required properties.
              This operation is non-idempotent.
        choices: ['present', 'absent', 'patch']
        required: true
        type: str
    data:
        description:
            - List with the repositories properties.
        required: true
        type: dict
    params:
        description:
            - Dict with query parameters.
        required: False
        type: dict
notes:
    - This resource is available for API version 300 or later.
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.validateetag
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Create a Repository
  oneview_repositories:
    config: "{{ config }}"
    state: present
    validate_etag: False
    data:
      repositoryName: "{{ repository_name }}"
      userName: "{{ repository_username }}"
      password: "{{ repository_password }}"
      repositoryURI: "{{ repository_uri }}"
      repositoryType: 'FirmwareExternalRepo'
  delegate_to: localhost
  register: repository

- name: Do nothing with the Repository when no changes are provided
  oneview_repositories:
    config: "{{ config }}"
    state: present
    data:
      repositoryName: "{{ repository_name }}"
      userName: "{{ repository_username }}"
      password: "{{ repository_password }}"
      repositoryURI: "{{ repository_uri }}"
      repositoryType: 'FirmwareExternalRepo'
  delegate_to: localhost

- name: Update the name of repository resource
  oneview_repositories:
    config: '{{ config }}'
    state: patch
    data:
      newName: "{{ repository_name }}-updated"
      name: "{{ repository_name }}"
  delegate_to: localhost

- name: Delete the Repository
  oneview_repositories:
    config: "{{ config }}"
    state: absent
    data:
      name: "{{ repository_name }}"
    params:
      force: True
  delegate_to: localhost
  register: deleted

- name: Do nothing when Repository is absent
  oneview_repositories:
    config: "{{ config }}"
    state: absent
    data:
      name: "{{ repository_name }}"
  delegate_to: localhost
  register: deleted
'''

RETURN = '''
repository:
    description: Has the facts about the Repository.
    returned: On state 'present' and 'patch', but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (OneViewModule, OneViewModuleResourceNotFound, compare, dict_merge,
                                                                          OneViewModuleValueError)


class RepositoriesModule(OneViewModule):
    MSG_CREATED = 'Repository created successfully.'
    MSG_UPDATED = 'Repository updated successfully.'
    MSG_ALREADY_PRESENT = 'Repository is already present.'
    MSG_RESOURCE_NOT_FOUND = 'Repository not found.'
    MSG_DELETED = 'Repository deleted successfully.'
    MSG_ALREADY_ABSENT = 'Repository is already absent.'
    MSG_CANT_UPDATE = 'Operation is not supported on Repository resource'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent', 'patch']
        ),
        data=dict(required=True, type='dict'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):

        super().__init__(additional_arg_spec=self.argument_spec,
                         validate_etag_support=True)

        self.set_resource_object(self.oneview_client.repositories)

    def execute_module(self):
        if self.state == 'present':
            return self.__present()
        elif self.state == 'absent':
            return self.__absent()
        elif self.state == 'patch':
            return self.__patch()

    def __present(self):
        changed = False

        if self.current_resource:
            response = self.__update()
        else:
            response = self.__create(self.data)

        return response

    def __create(self, data):
        if "name" in self.data:
            self.data["repositoryName"] = self.data.pop("name")
        self.current_resource = self.resource_client.create(data)
        changed = True
        return dict(changed=changed, msg=self.MSG_CREATED, ansible_facts=dict(repository=self.current_resource.data))

    def __update(self):
        changed = False
        parameter_to_ignore = ["userName", "password", "repositoryURI"]
        existing_data = self.current_resource.data.copy()
        updated_data = dict_merge(existing_data, self.data)

        if compare(self.current_resource.data, updated_data , parameter_to_ignore=parameter_to_ignore):
            msg = self.MSG_ALREADY_PRESENT
        else:
            response_patch = self.__patch()
            changed = True
            msg = self.MSG_UPDATED

        return dict(changed=changed, msg=msg, ansible_facts=dict(repository=self.current_resource.data))

    def __patch(self):
        # returns None if Repository doesn't exist
        if self.current_resource:
            if "newName" in self.data:
                self.data["name"] = self.data.pop("newName")
                self.current_resource.patch(operation='replace',
                                            path='/repositoryName',
                                            value=self.data['name'])
            else:
                raise OneViewModuleValueError(self.MSG_CANT_UPDATE)
        else:
            raise OneViewModuleResourceNotFound(self.MSG_RESOURCE_NOT_FOUND)

        return dict(changed=True,
                    msg=self.MSG_UPDATED,
                    ansible_facts=dict(repository=self.current_resource.data))

    def __absent(self):
        if self.current_resource:
            changed = True
            msg = self.MSG_DELETED
            self.current_resource.delete(**self.facts_params)
        else:
            changed = False
            msg = self.MSG_ALREADY_ABSENT
        return dict(changed=changed, msg=msg, ansible_facts=dict(repository=None))


def main():
    RepositoriesModule().run()


if __name__ == '__main__':
    main()
