#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2023-2024) Hewlett Packard Enterprise Development LP
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
module: oneview_drive_enclosure_facts
short_description: Retrieve facts about one or more Drive Enclosures
description:
    - Retrieve facts about one or more of the Drive Enclosures from OneView.
version_added: "2.5.0"
requirements:
    - hpeOneView >= 5.4.0
author:
    - Alisha K (@alisha-k-kalladassery)
options:
    name:
      description:
        - Drive Enclosure name.
      type: str
    uri:
      description:
        - Drive Enclosure uri.
      type: str
    sessionID:
      description:
        - Session ID to use for login to the appliance
      type: str
      required: false
    options:
      description:
        - "List with options to gather additional facts about a Drive Enclosure and related resources.
          Options allowed: C(port_map)"
      type: list
      elements: str

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Drive Enclosures
  oneview_drive_enclosure_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
  delegate_to: localhost

- debug: var=drive_enclosures

- name: Gather paginated, filtered and sorted facts about Drive Enclosures
  oneview_drive_enclosure_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=drive_enclosures

- name: Gather facts about an Enclosure by name
  oneview_drive_enclosure_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    name: "Drive Enclosure Name"
  delegate_to: localhost

- debug: var=drive_enclosures

- name: Gather Port map facts about a Drive Enclosure by name
  oneview_drive_enclosure_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    name: "Drive Enclosure Name"
    options:
      - port_map
  delegate_to: localhost

- debug: var=port_map
'''

RETURN = '''
drive_enclosures:
    description: Has all the OneView facts about the Drive Enclosures.
    returned: Always, but can be null.
    type: dict

port_map:
    description: Has all the OneView facts about Port Map of a Drive Enclosure.
    returned: When requested, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class DriveEnclosureFactsModule(OneViewModule):
    argument_spec = dict(name=dict(type='str'),
                         uri=dict(required=False, type='str'),
                         sessionID=dict(required=False, type='str'),
                         options=dict(type='list', elements='str'),
                         params=dict(type='dict'))

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, supports_check_mode=True)
        self.set_resource_object(self.oneview_client.drive_enclosures)

    def execute_module(self):

        ansible_facts = {}

        if self.current_resource:
            drive_enclosures = [self.current_resource.data]
            if self.options:
                ansible_facts = self._gather_optional_facts(self.options)
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            drive_enclosures = self.resource_client.get_all(**self.facts_params)
        else:
            drive_enclosures = []

        ansible_facts['drive_enclosures'] = drive_enclosures

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def _gather_optional_facts(self, options):

        ansible_facts = {}

        if options.get('port_map'):
            ansible_facts['port_map'] = self.current_resource.get_port_map()
        return ansible_facts


def main():
    DriveEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
