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
module: oneview_appliance_device_read_community_facts
short_description: Retrieve the facts about the OneView appliance device read community.
description:
    - Retrieve the facts about the OneView appliance device read community.
version_added: "2.9.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.4.0"
author:
    "Gianluca Zecchi (@gzecchi)"
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Gather facts about the Appliance snmp configuration
  oneview_appliance_device_read_community_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
- debug:
    var: appliance_device_read_community
'''

RETURN = '''
appliance_device_read_community:
    description: Has all the OneView facts about the OneView appliance device read community.
    returned: Always.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModuleBase


class ApplianceDeviceReadCommunityFactsModule(OneViewModuleBase):
    def __init__(self):
        super(ApplianceDeviceReadCommunityFactsModule, self).__init__(additional_arg_spec=dict())

    def execute_module(self):
        appliance_device_read_community = self.oneview_client.appliance_device_read_community.get()
        return dict(changed=False,
                    ansible_facts=dict(appliance_device_read_community=appliance_device_read_community))


def main():
    ApplianceDeviceReadCommunityFactsModule().run()


if __name__ == '__main__':
    main()
