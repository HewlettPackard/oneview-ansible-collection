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
module: oneview_sas_logical_interconnect_facts
short_description: Retrieve facts about one or more SAS Logical interconnects.
description:
    - Retrieve facts about one or more SAS Logical interconnects from OneView.
version_added: "2.5.0"
requirements:
    - hpeOneView >= 5.4.0
author:
    - Alisha K (@alisha-k-kalladassery)
options:
    name:
      description:
        - SAS Logical interconnect name
      type: str
    uri:
      description:
        - SAS Logical interconnect uri
      type: str
    sessionID:
      description:
        - Session ID to use for login to the appliance
      type: str
      required: false
    options:
      description:
        - "List with options to gather additional facts about a SAS Logical interconnect and related resources.
          Options allowed: C(firmware_facts)."
      type: list
      elements: str

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Fetch Session Id
  oneview_get_session_id:
    config: "{{ config }}"
    name: "Test_Session"
  delegate_to: localhost
  register: session

- debug: var=session

- name: Gather facts about all SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
  delegate_to: localhost

- debug: var=sas_logical_interconnects

- set_fact:
    sas_logical_interconnect_name: "{{ sas_logical_interconnects[0]['name'] }}"
- set_fact:
    sas_logical_interconnect_uri: "{{ sas_logical_interconnects[0]['uri'] }}"

- name: Gather paginated, filtered and sorted facts about SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=sas_logical_interconnects

- name: Gather facts about an SAS Logical interconnect by name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    name: "{{ sas_logical_interconnect_name }}"
  delegate_to: localhost

- debug: var=sas_logical_interconnects

- name: Gather facts about an SAS Logical interconnect by uri
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    uri: "{{ sas_logical_interconnect_uri }}"
  delegate_to: localhost

- debug: var=sas_logical_interconnects

- name: Gather baseline firmware facts about a SAS Logical interconnect by name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    name: "{{ sas_logical_interconnect_name }}"
    options:
      - firmware_facts
  delegate_to: localhost

- debug: var=firmware_facts
'''

RETURN = '''
sas_logical_interconnects:
    description: Has all the OneView facts about the SAS Logical Interconnects.
    returned: Always, but can be null.
    type: dict

firmware_facts:
    description: Has the baseline firmware information for a SAS logical interconnect.
    returned: When requested, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class SasLogicalInterconnectFactsModule(OneViewModule):
    argument_spec = dict(name=dict(type='str'),
                         uri=dict(required=False, type='str'),
                         sessionID=dict(required=False, type='str'),
                         options=dict(type='list', elements='str'),
                         params=dict(type='dict'))

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, supports_check_mode=True)
        self.set_resource_object(self.oneview_client.sas_logical_interconnects)

    def execute_module(self):

        ansible_facts = {}

        if self.current_resource:
            sas_logical_interconnects = [self.current_resource.data]
            if self.options:
                ansible_facts = self._gather_optional_facts(self.options)
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            sas_logical_interconnects = self.resource_client.get_all(**self.facts_params)
        else:
            sas_logical_interconnects = []

        ansible_facts['sas_logical_interconnects'] = sas_logical_interconnects

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def _gather_optional_facts(self, options):

        ansible_facts = {}

        if options.get('firmware_facts'):
            ansible_facts['firmware_facts'] = self.current_resource.get_firmware()

        return ansible_facts


def main():
    SasLogicalInterconnectFactsModule().run()


if __name__ == '__main__':
    main()
