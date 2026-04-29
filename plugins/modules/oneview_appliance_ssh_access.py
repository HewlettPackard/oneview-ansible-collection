#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021-2024, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_appliance_ssh_access
short_description: Retrieve the facts about the OneView appliance ssh access configuration.
description:
    - Retrieve the facts about the OneView appliance ssh access configuration.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author:
    "Shanmugam M (@SHANDCRUZ)"
options:
    sessionID:
        description:
          - Session ID to use for login to the appliance
        type: str
        required: false
    state:
        description:
            - Indicates the desired state for the Appliance SSH Access.
              C(present) will ensure data properties are compliant with OneView.
        choices: ['present']
        required: true
        type: str
    data:
        description:
            - List with the Appliance SSH Access properties.
        required: true
        type: dict

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Ensures the Appliance SSH Access is false
  oneview_appliance_ssh_access:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    state: present
    data:
      allowSshAccess: false
  delegate_to: localhost
- debug: var=appliance_ssh_access

- name: Ensures the Appliance SSH Access is true
  oneview_appliance_ssh_access:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    state: present
    data:
      allowSshAccess: true
  delegate_to: localhost
- debug: var=appliance_ssh_access
'''

RETURN = '''
appliance_ssh_access:
    description: Has all the OneView facts about the Appliance SSH Access.
    returned: Always.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class ApplianceSshAccessModule(OneViewModule):
    MSG_UPDATED = 'Appliance SSH Access updated successfully.'
    MSG_ALREADY_PRESENT = 'Appliance SSH Access is already updated.'
    RESOURCE_FACT_NAME = 'appliance_ssh_access'

    def __init__(self):
        additional_arg_spec = dict(sessionID=dict(required=False, type='str'),
                                   data=dict(required=True, type='dict'),
                                   state=dict(required=True, choices=['present']))
        super().__init__(additional_arg_spec=additional_arg_spec)
        self.set_resource_object(self.oneview_client.appliance_ssh_access)

    def execute_module(self):
        changed, msg, ansible_facts = False, '', {}
        self.current_resource = self.resource_client.get_all()
        changed, msg = self._update_resource()
        ansible_facts = dict(appliance_ssh_access=self.current_resource.data)

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=ansible_facts)


def main():
    ApplianceSshAccessModule().run()


if __name__ == '__main__':
    main()
