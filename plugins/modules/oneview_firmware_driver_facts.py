#!/usr/bin/python
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_firmware_driver_facts
short_description: Retrieve the facts about one or more of the OneView Firmware Drivers.
description:
    - Retrieve the facts about one or more of the Firmware Drivers from OneView.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    name:
      description:
        - Firmware driver name.
      required: false
      type: str
    uri:
      description:
        - Firmware driver uri.
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
        - "List with options to gather additional facts about Firmware driver related resource.
          Options allowed: C(schema)"
      required: false
      type: list

extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.factsparams
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about all Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=firmware_drivers

- name: Gather paginated, filtered and sorted facts about Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
  delegate_to: localhost

- debug: var=firmware_drivers

- name: Gather facts about a Firmware Driver by name
  oneview_firmware_driver_facts:
    config: "{{ config }}"
    name: "custom_firmware_bundle"
  delegate_to: localhost

- debug: var=firmware_drivers

- name: Gather facts about Firmware Driver with options
  oneview_firmware_driver_facts:
    config: "{{ config }}"
    options:
      - schema
  delegate_to: localhost

- debug: var=schema
'''

RETURN = '''
firmware_drivers:
    description: Has all the OneView facts about the Firmware Drivers.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class FirmwareDriverFactsModule(OneViewModule):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            uri=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict')
        )

        super().__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.firmware_drivers)

    def execute_module(self):
        ansible_facts = {}
        firmware_drivers = []

        if self.current_resource:
            firmware_drivers = self.current_resource.data
        elif self.options:
            if self.options.get('schema'):
                ansible_facts['schema'] = self.resource_client.get_schema()
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            firmware_drivers = self.resource_client.get_all(**self.facts_params)

        ansible_facts['firmware_drivers'] = firmware_drivers

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    FirmwareDriverFactsModule().run()


if __name__ == '__main__':
    main()
