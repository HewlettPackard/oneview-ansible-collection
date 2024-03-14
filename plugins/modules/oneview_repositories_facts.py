#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (2016-2024) Hewlett Packard Enterprise Development LP
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
module: oneview_repositories_facts
short_description: Retrieve facts about one or more of the OneView repositories.
description:
    - Retrieve facts about one or more of the repositories from OneView.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Chebrolu Harika (@ChebroluHarika)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false
      type: path
    name:
      description:
        - Name of the repository.
      required: false
      type: str
    sessionID:
      description:
        - Session ID to use for login to the appliance
      type: str
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
           c(start): The first item to return, using 0-based indexing.
           c(count): The number of resources to return.
           c(query): A general query string to narrow the list of resources returned.
           c(sort): The sort order of the returned data set.
           c(view): Returns a specific subset of the attributes of the resource or collection, by specifying the name
           of a predefined view."
      required: false
      type: dict
notes:
    - This resource is available for API version 300 or later.
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about all Repositories
  oneview_repositories_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=repositories

- name: Gather paginated, filtered and sorted facts about Repositories
  oneview_repositories_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'

- debug: var=repositories

- name: Gather facts about a Repository by Id
  oneview_repositories_facts:
    config: "{{ config }}"
    name: "{{ repositories[0]['uuid'] }}"
  delegate_to: localhost
  when: repositories | default('', True)

- debug: var=repositories

- name: Gather facts about a Repository by name
  oneview_repositories_facts:
    config: "{{ config }}"
    name: "{{ repositories[0]['name'] }}"
  delegate_to: localhost
  when: repositories | default('', True)

- debug: var=repositories
'''

RETURN = '''
repositories:
    description: Has all the OneView facts about the Repositories.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class RepositoriesFactsModule(OneViewModule):
    argument_spec = dict(
        sessionID=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, supports_check_mode=True)
        self.set_resource_object(self.oneview_client.repositories)

    def execute_module(self):
        if self.current_resource:
            repositories = [self.current_resource.data]
        else:
            repositories = self.resource_client.get_all(**self.facts_params)

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False, ansible_facts=dict(repositories=repositories))


def main():
    RepositoriesFactsModule().run()


if __name__ == '__main__':
    main()
