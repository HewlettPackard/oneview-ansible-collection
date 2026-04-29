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
module: oneview_version_facts
short_description: Returns the range of possible API versions supported by the appliance
description:
    - Provides an interface to return the range of possible API versions supported by the appliance.
version_added: "2.5.0"
requirements:
    - "hpeOneView >= 4.3.0"
author: "Priyanka Sood (@soodpr)"

options:
    sessionID:
        description:
            - Session ID to use for login to the appliance
        type: str
        required: false
extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about current and minimum Version
  oneview_version_facts:
    config: "{{ config_file_path }}"

- debug: var=version
'''

RETURN = '''
version:
    description: Has the facts about the OneView current and minimum version.
    returned: When requested, but can not be null
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModuleBase


class VersionFactsModule(OneViewModuleBase):
    def __init__(self):
        super().__init__(additional_arg_spec=dict(sessionID=dict(required=False, type='str')), supports_check_mode=True)

    def execute_module(self):
        version = self.oneview_client.versions.get_version()
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        return dict(changed=False,
                    ansible_facts=dict(version=version))


def main():
    VersionFactsModule().run()


if __name__ == '__main__':
    main()
