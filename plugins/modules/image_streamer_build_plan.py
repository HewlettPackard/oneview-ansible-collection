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
module: image_streamer_build_plan
short_description: Manages Image Stream OS Build Plan resources.
description:
    - "Provides an interface to manage Image Stream OS Build Plans. Can create, update, and remove."
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
        description:
            - Indicates the desired state for the OS Build Plan resource.
              C(present) will ensure data properties are compliant with Synergy Image Streamer.
              C(absent) will remove the resource from Synergy Image Streamer, if it exists.
        choices: ['present', 'absent']
        required: true
        type: str
    data:
        description:
            - List with OS Build Plan properties and its associated states.
        required: true
        type: dict
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Create an OS Build Plan
  image_streamer_build_plan:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "oebuildplan"
      oeBuildPlanType: "deploy"
  delegate_to: localhost
- name: Update the OS Build Plan description and name
  image_streamer_build_plan:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "New description"
      newName: 'OS Build Plan Renamed'
  delegate_to: localhost
- name: Remove an OS Build Plan
  image_streamer_build_plan:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    state: absent
    data:
        name: 'Demo OS Build Plan'
  delegate_to: localhost
'''

RETURN = '''
build_plan:
    description: Has the OneView facts about the OS Build Plan.
    returned: On state 'present'.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModuleBase, OneViewModuleValueError


class BuildPlanModule(OneViewModuleBase):
    MSG_CREATED = 'OS Build Plan created successfully.'
    MSG_UPDATED = 'OS Build Plan updated successfully.'
    MSG_ALREADY_PRESENT = 'OS Build Plan is already present.'
    MSG_DELETED = 'OS Build Plan deleted successfully.'
    MSG_ALREADY_ABSENT = 'OS Build Plan is already absent.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.build_plans

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])
        result = {}

        if self.state == 'present':
            result = self.resource_present(resource, 'build_plan')
        elif self.state == 'absent':
            result = self.resource_absent(resource)

        return result


def main():
    BuildPlanModule().run()


if __name__ == '__main__':
    main()
