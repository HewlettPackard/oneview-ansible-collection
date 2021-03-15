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
ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: oneview_appliance_device_snmp_v3_users
short_description: Manage the Appliance Device SNMPv3 Users.
description:
    - Provides an interface to manage the Appliance Device SNMPv3 Users.
version_added: "2.5.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.0.0"
author:
    "Nabhajit Ray (@nabhajit-ray)"
options:
    state:
        description:
          - Indicates the desired state for the Appliance Device SNMPv3 User.
            C(present) ensures data properties are compliant with OneView.
            C(absent) removes the resource from OneView, if it exists.
        choices: ['present', 'absent']
        type: str
        required: true
    name:
      description:
        - SNMP user name.
      type: str
    data:
        description:
            - List with the SNMPv3 Users properties
        required: false
        type: dict

extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Ensure that the SNMPv3 user is present using the default configuration
  oneview_appliance_device_snmp_v3_users:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
        type: "Users"
        userName: "testUser"
        securityLevel: "Authentication"
        authenticationProtocol: "SHA512"
  delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_users

- name: Set the password of specified SNMPv3 user
  oneview_appliance_device_snmp_v3_users:
   config: "{{ config }}"
   state: present
   name: "testUser"
   data:
    userName: "testUser"
    authenticationPassphrase: "NewPass1234"
    delegate_to: localhost

- debug:
    var: appliance_device_snmp_v3_users

- name: Ensure that the SNMPv3 user is absent
  oneview_appliance_device_snmp_v3_users:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: absent
    data:
        userName: "testUser"
  delegate_to: localhost
'''

RETURN = '''
appliance_device_snmp_v3_users:
    description: Has all the OneView facts about the OneView appliance SNMPv3 users.
    returned: On state 'present' and 'absent'.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (
    OneViewModule, OneViewModuleException,
    OneViewModuleValueError, OneViewModuleResourceNotFound
)


class ApplianceDeviceSnmpV3UsersModule(OneViewModule):
    MSG_CREATED = 'Appliance Device SNMPv3 User created successfully.'
    MSG_UPDATED = 'Appliance Device SNMPv3 User updated successfully.'
    MSG_DELETED = 'Appliance Device SNMPv3 User deleted successfully.'
    MSG_USER_NOT_FOUND = 'Appliance Device SNMPv3 User not found.'
    MSG_ALREADY_PRESENT = 'Appliance Device SNMPv3 User is already present.'
    MSG_ALREADY_ABSENT = 'Appliance Device SNMPv3 User is already absent.'
    MSG_VALUE_ERROR = 'The userName or the id attributes must be specfied'
    MSG_API_VERSION_ERROR = 'This module requires at least OneView 4.0 (API >= 600)'
    MSG_PASSWORD_UPDATED = 'User authenticationPassphrase set successfully.'
    RESOURCE_FACT_NAME = 'appliance_device_snmp_v3_users'

    def __init__(self):
        argument_spec = dict(
            data=dict(required=False, type='dict'),
            name=dict(required=False, type='str'),
            state=dict(
                required=True,
                choices=['present', 'absent']),
        )
        super().__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.appliance_device_snmp_v3_users)

    def execute_module(self):
        if self.oneview_client.api_version < 600:
            raise OneViewModuleValueError(self.MSG_API_VERSION_ERROR)
        if self.state == 'present':
            return self.resource_present(self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent()


def main():
    ApplianceDeviceSnmpV3UsersModule().run()


if __name__ == '__main__':
    main()
