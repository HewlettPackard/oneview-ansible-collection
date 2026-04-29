#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021-2024, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_appliance_time_and_locale_configuration
short_description: Manage OneView Appliance Locale and Time Configuration.
description:
    - Provides an interface to manage Appliance Locale and Time Configuration. It can only update it.
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
            - Indicates the desired state for the Appliance Locale and Time Configuration.
              C(present) will ensure data properties are compliant with OneView.
        choices: ['present']
        required: true
        type: str
    data:
        description:
            - List with the Appliance Locale and Time Configuration properties.
        required: true
        type: dict

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Ensure that the Appliance Locale and Time Configuration is present with locale 'en_US.UTF-8'
  oneview_appliance_time_and_locale_configuration:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2600
    state: present
    data:
      locale: 'en_US.UTF-8'
'''

RETURN = '''
appliance_time_and_locale_configuration:
    description: Has the facts about the OneView Appliance Locale and Time Configuration.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, compare


class ApplianceTimeAndLocaleConfigurationModule(OneViewModule):
    MSG_CREATED = 'Appliance Locale and Time Configuration configured successfully.'
    MSG_ALREADY_PRESENT = 'Appliance Locale and Time Configuration is already configured.'
    RESOURCE_FACT_NAME = 'appliance_time_and_locale_configuration'

    def __init__(self):
        additional_arg_spec = dict(sessionID=dict(required=False, type='str'),
                                   data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present']))

        super().__init__(additional_arg_spec=additional_arg_spec)
        self.resource_client = self.oneview_client.appliance_time_and_locale_configuration

    def execute_module(self):
        if self.state == 'present':
            changed, msg, appliance_time_and_locale_configuration = self.__present()
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        return dict(changed=changed, msg=msg, ansible_facts=appliance_time_and_locale_configuration)

    def __present(self):
        resource_data = {}
        self.current_resource = self.resource_client.get_all()
        if self.current_resource:
            resource_data = self.current_resource.data.copy()
        merged_data = resource_data.copy()
        merged_data.update(self.data)
        if not compare(resource_data, merged_data):
            self.current_resource = self.resource_client.create(self.data)
            return True, self.MSG_CREATED, dict(appliance_time_and_locale_configuration=self.current_resource.data)
        else:
            return False, self.MSG_ALREADY_PRESENT, dict(appliance_time_and_locale_configuration=self.current_resource.data)


def main():
    ApplianceTimeAndLocaleConfigurationModule().run()


if __name__ == '__main__':
    main()
