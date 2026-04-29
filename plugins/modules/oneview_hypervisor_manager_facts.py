#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021-2024, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_hypervisor_manager_facts
short_description: Retrieve the facts about one or more of the OneView Hypervisor Managers
description:
    - Retrieve the facts about one or more of the Hypervisor Managers from OneView.
version_added: "2.4.0"
requirements:
    - "python >= 2.7.9"
    - hpeOneView >= 5.4.0
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    sessionID:
      description:
        - Session ID to use for login to the appliance
      type: str
      required: false
    name:
      description:
        - Hypervisor Manager name.
      type: str
extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.factsparams
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about all Hypervisor Managers
  oneview_hypervisor_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
  delegate_to: localhost
- debug: var=hypervisor_managers
- name: Gather paginated, filtered and sorted facts about Hypervisor Managers
  oneview_hypervisor_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    params:
      start: 1
      count: 3
      sort: 'name:descending'
      filter: 'hypervisorType=Vmware'
  delegate_to: localhost
- debug: var=hypervisor_managers
- name: Gather facts about a Hypervisor Manager by name
  oneview_hypervisor_manager_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: hypervisor manager name
  delegate_to: localhost
- debug: var=hypervisor_managers
'''

RETURN = '''
hypervisor_manager:
    description: Has all the OneView facts about the Hypervisor Managers.
    returned: Always, but can be null.
    type: dict
'''
from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class HypervisorManagerFactsModule(OneViewModule):
    def __init__(self):

        argument_spec = dict(
            sessionID=dict(required=False, type='str'),
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super().__init__(additional_arg_spec=argument_spec, supports_check_mode=True)
        self.resource_client = self.oneview_client.hypervisor_managers

    def execute_module(self):

        if self.module.params['name']:
            hypervisor_managers = self.resource_client.get_by('name', self.module.params['name'])
        else:
            hypervisor_managers = self.resource_client.get_all(**self.facts_params)

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False, ansible_facts=dict(hypervisor_managers=hypervisor_managers))


def main():
    HypervisorManagerFactsModule().run()


if __name__ == '__main__':
    main()
