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
module: oneview_sas_interconnect_facts
short_description: Retrieve facts about one or more SAS Interconnects
description:
    - Retrieve facts about one or more SAS interconnects from OneView.
version_added: "2.5.0"
requirements:
    - hpeOneView >= 5.4.0
author:
    - Alisha K (@alisha-k-kalladassery)
options:
    name:
      description:
        - SAS Interconnect name
      type: str
    uri:
      description:
        - SAS Interconnect uri
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
---
- name: Fetch Session Id
  oneview_get_session_id:
    config: "{{ config }}"
    name: "Test_Session"
  delegate_to: localhost
  register: session

- debug: var=session

- name: Gather facts about all SAS Interconnects
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
  delegate_to: localhost

- debug: var=sas_interconnects

- set_fact:
    sas_interconnect_name: "{{ sas_interconnects[0]['name'] }}"
- set_fact:
    sas_interconnect_uri: "{{ sas_interconnects[0]['uri'] }}"

- name: Gather paginated, filtered and sorted facts about SAS Interconnects
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=sas_interconnects

- name: Gather facts about a SAS Interconnect by name
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    name: "{{ sas_interconnect_name }}"
  delegate_to: localhost

- debug: var=sas_interconnects

- name: Gather facts about a SAS Interconnect by uri
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    uri: "{{ sas_interconnect_uri }}"
  delegate_to: localhost

- debug: var=sas_interconnects
'''

RETURN = '''
sas_interconnects:
    description: Has all the OneView facts about the SAS Interconnects.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class SasInterconnectFactsModule(OneViewModule):
    argument_spec = dict(name=dict(type='str'), uri=dict(required=False, type='str'), sessionID=dict(required=False, type='str'), params=dict(type='dict'))

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, supports_check_mode=True)
        self.set_resource_object(self.oneview_client.sas_interconnects)

    def execute_module(self):

        ansible_facts = {}

        if self.current_resource:
            sas_interconnects = [self.current_resource.data]
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            sas_interconnects = self.resource_client.get_all(**self.facts_params)
        else:
            sas_interconnects = []

        ansible_facts['sas_interconnects'] = sas_interconnects

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False,
                    ansible_facts=ansible_facts)


def main():
    SasInterconnectFactsModule().run()


if __name__ == '__main__':
    main()
