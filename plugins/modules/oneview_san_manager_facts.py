# -*- coding: utf-8 -*-
###
# Copyright (2022-2024) Hewlett Packard Enterprise Development LP
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
module: oneview_san_manager_facts
short_description: Retrieve facts about the OneView San Manager.
description:
    - Retrieve facts about the San Manager from OneView.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Nabhajit Ray (@nabhajit-ray)"
options:
    name:
      description:
        - san Manager name.
      required: false
      type: str
    sessionID:
      description:
        - Session ID to use for login to the appliance
      type: str
      required: false
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all San Managers
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4600
  delegate_to: localhost
- debug: var=san_managers
- set_fact:
    san_manager_name: "{{ san_managers[0]['name'] }}"
- set_fact:
    san_manager_uri: "{{ san_managers[0]['uri'] }}"
- debug: var=san_manager_name
- name: Gather paginated, filtered and sorted facts about san Manager
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4600
    params:
      start: 0
      count: 2
      sort: name:ascending
      filter: 'refreshState=Stable'
  delegate_to: localhost
- debug: msg="{{san_managers | map(attribute='name') | list }}"
- name: Gather facts about a San Manager by name
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4600
    name: "{{ san_manager_name }}"
  delegate_to: localhost
'''

RETURN = '''
san_managers:
    description: Has all the OneView facts about all the San Managers.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class SanManagerFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
            sessionID=dict(required=False, type='str'),
        )
        super().__init__(additional_arg_spec=argument_spec, supports_check_mode=True)
        self.set_resource_object(self.oneview_client.san_managers)
        self.san_providers = self.oneview_client.san_providers

    def execute_module(self):

        name = self.module.params.get('name')
        if name:
            san_managers = self.resource_client.get_by('name', name)
        else:
            san_managers = self.resource_client.get_all(**self.facts_params)

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False,
                    ansible_facts=dict(san_managers=san_managers))


def main():
    SanManagerFactsModule().run()


if __name__ == '__main__':
    main()
