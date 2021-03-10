#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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
module: image_streamer_deployment_plan_facts
short_description: Retrieve facts about the Image Streamer Deployment Plans.
description:
    - Retrieve facts about one or more of the Image Streamer Deployment Plans.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author:
    - "Venkatesh Ravula (@VenkateshRavula)"
options:
    name:
      description:
        - Deployment Plan name.
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
        - "List with options to gather additional facts about Deployment Plan related resource.
          Options allowed:
            C(osdp)
            C(usedby)"
      required: false
      type: str

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.factsparams
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about all Deployment Plans
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2010
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather paginated, filtered and sorted facts about Deployment Plans
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2010
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=active
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather facts about a Deployment Plan by name
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2010
    name: "Demo Deployment Plan"
  delegate_to: localhost
- debug: var=deployment_plans

- name: Gather facts about Server Profiles and Server Profile Templates that are using Deployment Plan
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2010
    name: "Demo Deployment Plan"
    options: "usedby"
  delegate_to: localhost
- debug: var=deployment_plans

- name: Get the OS deployment plan details from OneView for a deployment plan
  image_streamer_deployment_plan_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2010
    name: "Demo Deployment Plan"
    options: "osdp"
  delegate_to: localhost
- debug: var=deployment_plans
'''

RETURN = '''
deployment_plans:
    description: The list of Deployment Plans.
    returned: Always, but can be null.
    type: list
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class DeploymentPlanFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")
        options = self.module.params.get("options")
        ansible_facts = {}
        if name:
            ansible_facts['deployment_plans'] = self.i3s_client.deployment_plans.get_by("name", name)
            if ansible_facts['deployment_plans'] and options == 'usedby':
                deployment_plan = ansible_facts['deployment_plans'][0]
                environmental_configuration = self.i3s_client.deployment_plans.get_usedby(deployment_plan['uri'])
                ansible_facts['deployment_plans'][0]['deployment_plan_usedby'] = environmental_configuration
            elif ansible_facts['deployment_plans'] and options == 'osdp':
                deployment_plan = ansible_facts['deployment_plans'][0]
                environmental_configuration = self.i3s_client.deployment_plans.get_osdp(deployment_plan['uri'])
                ansible_facts['deployment_plans'][0]['deployment_plan_osdp'] = environmental_configuration
        else:
            ansible_facts['deployment_plans'] = self.i3s_client.deployment_plans.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    DeploymentPlanFactsModule().run()


if __name__ == '__main__':
    main()
