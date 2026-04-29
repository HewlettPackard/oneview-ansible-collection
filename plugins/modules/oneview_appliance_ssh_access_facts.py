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
module: oneview_appliance_ssh_access_facts
short_description: Retrieve the facts about the OneView appliance SSH access configuration.
description:
    - Retrieve the facts about the OneView appliance SSH access configuration.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
options:
    sessionID:
        description:
          - Session ID to use for login to the appliance
        type: str
        required: false
author:
    "Shanmugam M (@SHANDCRUZ)"
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about the Appliance SSH Access
  oneview_appliance_ssh_access_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    delegate_to: localhost

- debug: var=appliance_ssh_access
'''

RETURN = '''
appliance_ssh_access:
    description: Has all the OneView facts about the Appliance SSH access.
    returned: Always.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class ApplianceSshAccessFactsModule(OneViewModule):
    def __init__(self):
        super().__init__(additional_arg_spec=dict(sessionID=dict(required=False, type='str')), supports_check_mode=True)
        self.set_resource_object(self.oneview_client.appliance_ssh_access)

    def execute_module(self):
        appliance_ssh_access = self.resource_client.get_all()
        appliance_ssh_access = appliance_ssh_access.data
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        return dict(changed=False,
                    ansible_facts=dict(appliance_ssh_access=appliance_ssh_access))


def main():
    ApplianceSshAccessFactsModule().run()


if __name__ == '__main__':
    main()
