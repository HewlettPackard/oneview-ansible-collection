#!/usr/bin/python
# -*- coding: utf-8 -*-
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
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present']))

        super().__init__(additional_arg_spec=additional_arg_spec)
        self.resource_client = self.oneview_client.appliance_time_and_locale_configuration

    def execute_module(self):
        if self.state == 'present':
            changed, msg, appliance_time_and_locale_configuration = self.__present()
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
