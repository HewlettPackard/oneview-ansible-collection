#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2021-2024) Hewlett Packard Enterprise Development LP
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
module: oneview_appliance_proxy_configuration_facts
short_description: Retrieve the facts about the OneView appliance proxy configuration.
description:
    - Retrieve the facts about the OneView appliance proxy configuration.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.3.0"
author:
    "Yuvarani Chidambaram (@yuvirani)"
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
- name: Gather facts about the Appliance Proxy
  oneview_appliance_proxy_configuration_facts:
    config: "{{ config }}"
  delegate_to: localhost
'''

RETURN = '''
appliance_proxy_configuration:
    description: Has all the OneView facts about the Appliance Proxy Configuration.
    returned: Always.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class ApplianceProxyConfigurationFactsModule(OneViewModule):
    def __init__(self):
        super().__init__(additional_arg_spec=dict(sessionID=dict(required=False, type='str')), supports_check_mode=True)
        self.set_resource_object(self.oneview_client.appliance_proxy_configuration)

    def execute_module(self):
        proxy_configuration = self.resource_client.get_all()

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False,
                    ansible_facts=dict(appliance_proxy_configuration=proxy_configuration.data))


def main():
    ApplianceProxyConfigurationFactsModule().run()


if __name__ == '__main__':
    main()
