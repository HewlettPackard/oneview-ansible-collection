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
module: oneview_task_facts
short_description: Retrieve facts about the OneView Tasks.
description:
    - Retrieve facts about the OneView Tasks.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Bruno Souza (@bsouza)"
options:
    params:
      description:
        - "List with parameters to help filter the tasks.
          Params allowed: C(count), C(fields), C(filter), C(query), C(sort), C(start), and C(view)."
      required: false
      type: dict

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about the last 2 tasks
  oneview_task_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    params:
      count: 2

- debug: var=tasks

- name: Gather facts about the last 2 tasks associated to Server Profile templates
  oneview_task_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
    params:
      count: 2
      filter: "associatedResource.resourceCategory='server-profile-templates'"

- debug: var=tasks
'''

RETURN = '''
tasks:
    description: The list of tasks.
    returned: Always, but can be null.
    type: list
'''

from plugins.module_utils.oneview import OneViewModule


class TaskFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            params=dict(required=False, type='dict')
        )
        super().__init__(additional_arg_spec=argument_spec)

        self.set_resource_object(self.oneview_client.tasks)

    def execute_module(self):
        facts = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(tasks=facts))


def main():
    TaskFactsModule().run()


if __name__ == '__main__':
    main()
