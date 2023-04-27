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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_label
short_description: Manage OneView Label resources.
description:
    - Provides an interface to manage Label resources. Can create, update, or delete.
version_added: "2.5.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 6.1.0"
    - "ansible >= 2.9"
author: "Asis Bagga (@asisbagga)"
options:
    sessionID:
        description:
            - Session ID to use for login to the appliance
        type: str
        required: false
    logout:
        description:
            - Param to logout from the appliance when the task is done.
        type: bool
        required: false
    state:
        description:
            - Indicates the desired state for the label resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        type: str
        required: true
    data:
        description:
            - List with Label properties.
        required: true
        type: dict

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.validateetag
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Create Labels for enclosure reosurces
  oneview_label:
    config: "{{ config }}"
    state: present
    data:
      resourceUri: "/rest/enclosures/0000000000A66102"
      labels:
        - name: "Test label 1"
        - name: "Test Label 2"
  delegate_to: localhost
  register: label
- debug: var=label

- name: Update label of given reosurce for enclosure reosurces
  oneview_label:
    config: "{{ config }}"
    state: present
    data:
      resourceUri: "/rest/enclosures/0000000000A66102"
      labels:
        - name: "Test label 1 Renamed"
          uri: null
        - name: "Test label 2 Renamed"
          uri: null
        - name: "Test label 3"
          uri: null
  delegate_to: localhost
  register: label
- debug: var=label

- name: Delete Labels for enclosure reosurces
  oneview_label:
    config: "{{ config }}"
    state: absent
    data:
      resourceUri: "/rest/enclosures/0000000000A66102"
  delegate_to: localhost
  register: label
- debug: var=label
'''

RETURN = '''
label:
    description: Has the facts about the OneView label.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class LabelModule(OneViewModule):
    MSG_CREATED = 'Label created successfully.'
    MSG_UPDATED = 'Label updated successfully.'
    MSG_DELETED = 'Label deleted successfully.'
    MSG_ALREADY_PRESENT = 'Label is already present.'
    MSG_ALREADY_ABSENT = 'Label is already absent.'
    RESOURCE_FACT_NAME = 'labels'

    def __init__(self):
        additional_arg_spec = dict(sessionID=dict(required=False, type='str'),
                                   logout=dict(required=False, type='bool'),
                                   data=dict(required=True, type='dict'),
                                   state=dict(required=True, choices=['present', 'absent']))
        super().__init__(additional_arg_spec=additional_arg_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.labels

    def execute_module(self):
        self.current_resource = None
        if self.state == 'present':
            result = self._present()
            if self.module.params.get('logout'):
                self.oneview_client.connection.logout()
            return result
        elif self.state == 'absent':
            self.current_resource = self.resource_client.get_by_resource(self.data.get('resourceUri'))
            result = self.resource_absent()
            if self.module.params.get('logout'):
                self.oneview_client.connection.logout()
            return result

    def _present(self):
        if self.data.get('resourceUri'):
            all_labels = self.resource_client.get_by_resource(self.data.get('resourceUri'))
            if all_labels.data['labels']:
                self.current_resource = all_labels
            result = self.resource_present(self.RESOURCE_FACT_NAME)
        return result


def main():
    LabelModule().run()


if __name__ == '__main__':
    main()
