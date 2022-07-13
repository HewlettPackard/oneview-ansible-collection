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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_connection_template_facts
short_description: Retrieve facts about the OneView Connection Templates.
version_added: "2.3.0"
description:
    - Retrieve facts about the OneView Connection Templates.
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Connection Template name.
      required: false
      type: str
    options:
      description:
        - "List with options to gather additional facts about Connection Template related resources.
           Options allowed:
           C(defaultConnectionTemplate)."
      required: false
      type: list

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Connection Templates
  oneview_connection_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
  delegate_to: localhost
- debug: var=connection_templates

- name: Gather paginated, filtered and sorted facts about Connection Templates
  oneview_connection_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=defaultConnectionTemplate'

- debug: var=connection_templates

- name: Gather facts about a Connection Template by name
  oneview_connection_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    name: 'connection template name'
  delegate_to: localhost
- debug: var=connection_templates

- name: Gather facts about the Default Connection Template
  oneview_connection_template_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    options:
      - defaultConnectionTemplate
  delegate_to: localhost
- debug: var=default_connection_template
'''

RETURN = '''
connection_templates:
    description: Has all the OneView facts about the Connection Templates.
    returned: Always, except when defaultConnectionTemplate is requested. Can be null.
    type: dict

default_connection_template:
    description: Has the facts about the Default Connection Template.
    returned: When requested, but can be null.
    type: dict
'''


from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class ConnectionTemplateFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict')
        )
        super().__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.connection_templates)

    def execute_module(self):
        ansible_facts = {}

        if 'defaultConnectionTemplate' in self.options:
            ansible_facts['default_connection_template'] = self.resource_client.get_default()
        elif self.module.params.get('name'):
            ansible_facts['connection_templates'] = self.get_by_name(self.module.params['name'])
        else:
            ansible_facts['connection_templates'] = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=ansible_facts)


def main():
    ConnectionTemplateFactsModule().run()


if __name__ == '__main__':
    main()
