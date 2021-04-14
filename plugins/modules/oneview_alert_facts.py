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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_alert_facts
short_description: Retrieve facts about the OneView Alerts.
description:
    - Retrieve facts about the OneView Alerts.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.4.0"
author: "Andressa Cruz (@asserdna)"
options:
    params:
      description:
        - "List with parameters to help filter the alerts.
          Params allowed: C(count), C(fields), C(filter), C(query), C(sort), C(start), and C(view)."
      required: false
      type: dict

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.factsparams
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about the last 2 alerts
  oneview_alert_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    params:
      count: 2

- debug: var=alerts

- name: Gather facts about the alerts with state 'Cleared'
  oneview_alert_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    params:
      count: 2
      filter: "alertState='Cleared'"

- debug: var=alerts

- name: Gather facts about the alerts with urgency 'High'
  oneview_alert_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 600
    params:
      count: 5
      filter: "urgency='High'"

- debug: var=alerts
'''

RETURN = '''
alerts:
    description: The list of alerts.
    returned: Always, but can be null.
    type: list
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModuleBase


class AlertFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            params=dict(required=False, type='dict')
        )
        super(AlertFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        facts = self.oneview_client.alerts.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(alerts=facts))


def main():
    AlertFactsModule().run()


if __name__ == '__main__':
    main()
