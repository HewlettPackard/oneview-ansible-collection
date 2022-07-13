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
module: oneview_interconnect_type_facts
short_description: Retrieve facts about one or more of the OneView Interconnect Types.
description:
    - Retrieve facts about one or more of the Interconnect Types from OneView.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Interconnect Type name.
      required: false
      type: str
extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.factsparams
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about all Interconnect Types
  oneview_interconnect_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200

- debug: var=interconnect_types

- name: Gather paginated, filtered and sorted facts about Interconnect Types
  oneview_interconnect_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "maximumFirmwareVersion='4000.99'"

- debug: var=interconnect_types

- name: Gather facts about an Interconnect Type by name
  oneview_interconnect_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: HP VC Flex-10 Enet Module

- debug: var=interconnect_types
'''

RETURN = '''
interconnect_types:
    description: Has all the OneView facts about the Interconnect Types.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class InterconnectTypeFactsModule(OneViewModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.interconnect_types

    def execute_module(self):

        if self.module.params.get('name'):
            interconnect_types = self.resource_client.get_by("name", self.module.params['name'])
        else:
            interconnect_types = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(interconnect_types=interconnect_types))


def main():
    InterconnectTypeFactsModule().run()


if __name__ == '__main__':
    main()
