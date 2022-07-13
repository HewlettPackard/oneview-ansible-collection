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
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: image_streamer_plan_script_facts
short_description: Retrieve facts about the Image Streamer Plan Scripts.
description:
    - Retrieve facts about one or more of the Image Streamer Plan Script.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author:
    - "Venkatesh Ravula (@VenkateshRavula)"
options:
    name:
      description:
        - Plan Script name.
      required: false
      type: str
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(sort): The sort order of the returned data set."
      required: false
      type: dict
    options:
      description:
        - "List with options to gather additional facts about image streamer plan script resources.
          Options allowed: C(getUseby)."
      required: false
      type: list

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Plan Scripts
  image_streamer_plan_script_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
  delegate_to: localhost
- debug: var=plan_scripts
- name: Gather paginated, filtered and sorted facts about Plan Scripts
  image_streamer_plan_script_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: planType=capture
  delegate_to: localhost
- debug: var=plan_scripts
- name: Gather facts about a Plan Script by name
  image_streamer_plan_script_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    image_streamer_hostname: 172.16.101.48
    name: "Demo Plan Script"
  delegate_to: localhost
- debug: var=plan_scripts
'''

RETURN = '''
plan_scripts:
    description: The list of Plan Scripts.
    returned: Always, but can be null.
    type: list
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModuleBase


class PlanScriptFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        ansible_facts = {}

        if name:
            plan_scripts = self.i3s_client.plan_scripts.get_by("name", name)
        else:
            plan_scripts = self.i3s_client.plan_scripts.get_all(**self.facts_params)

        ansible_facts['plan_scripts'] = plan_scripts

        if self.options:
            ansible_facts.update(self._get_options_facts(plan_scripts))

        return dict(changed=False, ansible_facts=ansible_facts)

    def _get_options_facts(self, plan_script):
        options_facts = {}

        if self.options.get("getUseby") and plan_script:
            options_facts["use_by"] = self.i3s_client.plan_scripts.get_usedby_and_readonly(plan_script[0]["id"])

        return options_facts


def main():
    PlanScriptFactsModule().run()


if __name__ == '__main__':
    main()
