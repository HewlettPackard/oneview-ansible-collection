#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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
module: oneview_logical_enclosure_facts
short_description: Retrieve facts about one or more of the OneView Logical Enclosures.
description:
    - Retrieve facts about one or more of the Logical Enclosures from OneView.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Logical Enclosure name.
      required: false
      type: str
    options:
      description:
        - "List with options to gather additional facts about a Logical Enclosure and related resources.
          Options allowed: script."
      required: false
      type: list

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Enclosures
  oneview_logical_enclosure_facts:
      hostname: 172.16.101.48
      username: administrator
      password: my_password
      api_version: 2000
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather paginated, filtered and sorted facts about Logical Enclosures
  oneview_logical_enclosure_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'
      scope_uris: '/rest/scope/637fa556-a78d-4796-8fce-2179e249ea7d'

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    name: "Encl1"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name with options
  oneview_logical_enclosure_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    name: "Encl1"
    options:
      - script
  delegate_to: localhost

- debug: var=logical_enclosures
- debug: var=logical_enclosure_script
'''

RETURN = '''
logical_enclosures:
    description: Has all the OneView facts about the Logical Enclosures.
    returned: Always, but can be null.
    type: dict

logical_enclosure_script:
    description: Has the facts about the script of a Logical Enclosure.
    returned: When required, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class LogicalEnclosureFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.oneview_client.logical_enclosures)

    def execute_module(self):
        ansible_facts = {}

        if self.module.params.get('name'):
            logical_enclosures = self.current_resource.data if self.current_resource else []
            if self.options and logical_enclosures:
                ansible_facts = self.__gather_optional_facts()
        else:
            logical_enclosures = self.resource_client.get_all(**self.facts_params)

        ansible_facts['logical_enclosures'] = logical_enclosures

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_optional_facts(self):
        ansible_facts = {}

        if self.options.get('script'):
            ansible_facts['logical_enclosure_script'] = self.current_resource.get_script()

        return ansible_facts


def main():
    LogicalEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
