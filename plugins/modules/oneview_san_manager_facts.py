#!/usr/bin/python
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
module: oneview_san_manager_facts
short_description: Retrieve facts about the OneView san Manager.
description:
    - Retrieve facts about the san Manager from OneView.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Alisha Kalladassery (@alisha-k-kalladassery)"
options:
    name:
      description:
        - san Manager name.
      required: false
      type: str
    options:
      description:
        - "List with options to gather additional facts about san Manager related resources.
          Options allowed: C(chassis), C(managers), C(partitions), C(environmental_configuration),
          C(remote_support_settings)."
      required: false
      type: list
    uri:
      description:
        - san Manager Uri
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
- name: Gather facts about all san Managers
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4400
  delegate_to: localhost
- debug: var=san_managers
- set_fact:
    san_manager_name : "{{ san_managers[0]['name'] }}"
- set_fact:
    san_manager_uri : "{{ san_managers[0]['uri'] }}"
- debug: var=san_manager_name
- name: Gather facts about all san Managers
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4400
    options:
      - chassis
      - partitions
      - managers
  delegate_to: localhost
- debug: var=all_chassis
- debug: var=all_partitions
- debug: var=all_managers
- name: Gather paginated, filtered and sorted facts about san Manager
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4400
    params:
      start: 0
      count: 2
      sort: name:ascending
      filter: state='Monitored'
  delegate_to: localhost
- debug: msg="{{san_managers | map(attribute='name') | list }}"
- name: Gather facts about a san Manager by name
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4400
    name: "{{ san_manager_name }}"
  delegate_to: localhost
- name: Gather facts about a san manager by uri
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4400
    uri: "{{ san_manager_uri }}"
  delegate_to: localhost
- name: Gather chassis facts about a san manager
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4400
    name: "{{ san_manager_name }}"
    options:
      - chassis
  delegate_to: localhost
- name: Gather all facts about a san Manager
  oneview_san_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 4400
    name: "{{ san_manager_name }}"
    options:
      - chassis                       # optional
      - partitions                    # optional
      - managers                      # optional
      - environmental_configuration   # optional
      - remote_support_settings       # optional
  delegate_to: localhost
- debug: var=san_manager_chassis
- debug: var=san_manager_partitions
- debug: var=san_manager_managers
- debug: var=san_manager_env_conf
- debug: var=san_manager_remote_support
'''

RETURN = '''
san_managers:
    description: Has all the OneView facts about all the san Managers.
    returned: Always, but can be null.
    type: dict
all_chassis:
    description: Has all the OneView facts about Chassis in all san Managers.
    returned: Always, but can be null.
    type: dict
all_partitions:
    description: Has all the OneView facts about Partitions in all san Managers.
    returned: Always, but can be null.
    type: dict
all_managers:
    description: Has all the OneView facts about Managers in all san Managers.
    returned: Always, but can be null.
    type: dict
san_manager_chassis:
    description: Has all the OneView facts about Chassis in a san Manager.
    returned: Always, but can be null.
    type: dict
san_manager_partitions:
    description: Has all the OneView facts about Partitions in a san Manager.
    returned: Always, but can be null.
    type: dict
san_manager_managers:
    description: Has all the OneView facts about Managers in a san Manager.
    returned: Always, but can be null.
    type: dict
san_manager_env_conf:
    description: Has all the OneView facts about Environmental Configuration in a san Manager.
    returned: Always, but can be null.
    type: dict
san_manager_remote_support:
    description: Has all the OneView facts about Remote Support Settings in a san Manager.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class SanManagerFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            uri=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
            sessionID=dict(required=False, type='str'),
        )
        super().__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.san_managers)
        self.san_providers = self.oneview_client.san_providers
  
    def execute_module(self):

        name = self.module.params.get('name')        
        if  name:
            san_managers = self.resource_client.get_by('name', name)
        else:
            san_managers = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(san_managers=san_managers))

    # def execute_module(self):
    #     ansible_facts = {}
    #     san_managers = []

    #     if self.module.params.get('name') or self.module.params.get('uri'):
    #         if self.current_resource:
    #             san_managers = self.current_resource.data
    #             if self.options:
    #                 ansible_facts = self.gather_option_facts()
    #     # else:
    #     #     if self.options and self.options.get('chassis'):
    #     #         ansible_facts['all_chassis'] = self.oneview_client.san_managers.get_all_chassis()
    #     #     if self.options and self.options.get('managers'):
    #     #         ansible_facts['all_managers'] = self.oneview_client.san_managers.get_all_managers()
    #     #     if self.options and self.options.get('partitions'):
    #     #         ansible_facts['all_partitions'] = self.oneview_client.san_managers.get_all_partitions()

    #     #     san_managers = self.resource_client.get_all(**self.facts_params)

    #     ansible_facts["san_managers"] = san_managers

    #     return dict(changed=False, ansible_facts=ansible_facts)

    # def gather_option_facts(self):
    #     ansible_facts = {}

    #     # if self.options.get('chassis'):
    #     #     ansible_facts['san_manager_chassis'] = self.current_resource.get_associated_chassis()

    #     # if self.options.get('partitions'):
    #     #     ansible_facts['san_manager_partitions'] = self.current_resource.get_associated_partitions()

    #     # if self.options.get('managers'):
    #     #     ansible_facts['san_manager_managers'] = self.current_resource.get_associated_managers()

    #     # if self.options.get('environmental_configuration'):
    #     #     ansible_facts['san_manager_env_conf'] = self.current_resource.get_environmental_configuration()

    #     # if self.options.get('remote_support_settings'):
    #     #     ansible_facts['san_manager_remote_support'] = self.current_resource.get_remote_support_settings()

    #     return ansible_facts


def main():
    SanManagerFactsModule().run()


if __name__ == '__main__':
    main()