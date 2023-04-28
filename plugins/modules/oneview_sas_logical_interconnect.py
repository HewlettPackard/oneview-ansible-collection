#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2023) Hewlett Packard Enterprise Development LP
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
module: oneview_sas_logical_interconnect
short_description: Manage OneView SAS Logical Interconnect resources.
description:
    - Provides an interface to manage SAS Logical Interconnect resources.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.6.0"
author: "Alisha K (@alisha-k-kalladassery)"
options:
    sessionID:
        description:
            - Session ID to use for login to the appliance
        type: str
        required: false
    logout:
      description:
        - Param to logout from the appliance when the task is done.
      type: bool
      required: false
    state:
        description:
            - Indicates the desired state for the Logical Interconnect resource.
              C(compliance) brings the sas logical interconnect back to a consistent state.
              C(apply_configuration) Asynchronously applies or re-applies the logical interconnect configuration.
              C(update_firmware) Installs firmware to the member interconnects of a logical interconnect.
              C(replace_drive_enclosure) Initiate the replacement operation that enables the new drive enclosure to take \
                over as a replacement for the prior drive enclosure.
        choices: ['compliance', 'apply_configuration', 'update_firmware', 'replace_drive_enclosure']
        type: str
        required: true
    data:
        description:
            - List with the options.
        required: true
        type: dict

extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Fetch Session Id
  oneview_get_session_id:
    config: "{{ config }}"
    name: "Test_Session"
  delegate_to: localhost
  register: session

- debug: var=session

- name: Gather facts about all SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
  delegate_to: localhost

- set_fact:
    sas_logical_interconnect_name : "{{ sas_logical_interconnects[0]['name'] }}"

- name: Return the SAS Logical Interconnect to a consistent state
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: compliance
    data:
      name: "{{ sas_logical_interconnect_name }}"
  delegate_to: localhost
  register: result
- debug: var=result.msg

- name: Update the configuration on the logical interconnect
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: apply_configuration
    data:
      name: "{{ sas_logical_interconnect_name }}"
  delegate_to: localhost
  register: result
- debug: var=result.msg

- name: Gather facts about all Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
  delegate_to: localhost

- debug: var=firmware_drivers

- name: Installs firmware to the member interconnects of a logical interconnect
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: update_firmware
    data:
      name: "{{ sas_logical_interconnect_name }}"
      firmware:
        command: "Stage"
        force: false
        sppUri: "{{ firmware_drivers[0]['uri'] }}"
  when: firmware_drivers is defined
  delegate_to: localhost

- name: Replace Drive Enclosure (This example only works with real hardware)
  oneview_sas_logical_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: replace_drive_enclosure
    data:
      name: "{{ sas_logical_interconnect_name }}"
      driveReplaceConfig:
        oldSerialNumber: "SN1100"
        newSerialNumber: "SN1101"
'''

RETURN = '''
sas_logical_interconnect:
    description: Has the OneView facts about the SAS Logical Interconnect.
    returned: On 'compliance', 'apply_configuration', 'replace_drive_enclosure' states, but can be null.
    type: dict

update_firmware:
    description: Has the OneView facts about the SAS Logical interconnect firmware.
    returned: On 'update_firmware' state, but can be null.
    type: dict
'''

import time
from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, OneViewModuleResourceNotFound, OneViewModuleValueError, compare


class SasLogicalInterconnectModule(OneViewModule):
    MSG_CONSISTENT = 'SAS Logical Interconnect returned to a consistent state.'
    MSG_CONFIGURATION_UPDATED = 'Applied/Re-applied the logical interconnect configuration to all managed interconnects of the Logical Interconnect.'
    MSG_FIRMWARE_INSTALLED = 'Firmware updated successfully.'
    MSG_NOT_FOUND = 'SAS Logical Interconnect not found.'
    MSG_NO_OPTIONS_PROVIDED = 'No options provided.'
    MSG_DRIVE_ENCLOSURE_REPLACED = 'Drive Enclosure replaced successfully.'

    argument_spec = dict(
        sessionID=dict(required=False, type='str'),
        logout=dict(required=False, type='bool'),
        state=dict(
            required=True,
            choices=['compliance', 'apply_configuration', 'update_firmware', 'replace_drive_enclosure']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec,
                         validate_etag_support=True)
        self.set_resource_object(self.oneview_client.sas_logical_interconnects)

    def execute_module(self):

        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_NOT_FOUND)

        changed, msg, ansible_facts = False, '', dict()

        if self.state == 'compliance':
            changed, msg, ansible_facts = self.__compliance()
        elif self.state == 'apply_configuration':
            changed, msg, ansible_facts = self.__apply_configuration()
        elif self.state == 'install_firmware':
            changed, msg, ansible_facts = self.__install_firmware()
        elif self.state == 'replace_drive_enclosure':
            changed, msg, ansible_facts = self.__replace_drive_enclosure()

        if ansible_facts:
            result = dict(changed=changed, msg=msg, ansible_facts=ansible_facts)
        else:
            result = dict(changed=changed, msg=msg)

        if self.module.params.get('logout'):
            self.oneview_client.connection.logout()

        return result

    def __compliance(self):
        # This block will handle the exception caused by parallel operations made on same resource
        try:
            resource = self.current_resource.update_compliance()
            return True, self.MSG_CONSISTENT, dict(sas_logical_interconnect=resource)
        except Exception as e:
            attrib_val = getattr(e, 'oneview_response', None)
            if attrib_val and attrib_val.get('errorCode') == 'CRM_ONGOING_OPERATION_ON_LOGICAL_INTERCONNECT':
                time.sleep(60)
                main()
            else:
                raise e

    def __apply_configuration(self):
        result = self.current_resource.update_configuration()

        return True, self.MSG_CONFIGURATION_UPDATED, dict(sas_logical_interconnect=result)

    def __install_firmware(self):
        self.__validate_options('firmware', self.data)

        options = self.data['firmware'].copy()
        if 'spp' in options:
            options['sppUri'] = self.__build_firmware_uri(options.pop('spp'))

        firmware = self.current_resource.update_firmware(options)

        return True, self.MSG_FIRMWARE_INSTALLED, dict(li_firmware=firmware)

    def __replace_drive_enclosure(self):
        self.__validate_options('driveReplaceConfig', self.data)

        options = self.data['driveReplaceConfig'].copy()

        resource = self.current_resource.replace_drive_enclosure(options)

        return True, self.MSG_DRIVE_ENCLOSURE_REPLACED, dict(drive_replacement_output=resource)

    def __validate_options(self, subresource_type, data):
        if subresource_type not in data:
            raise OneViewModuleValueError(self.MSG_NO_OPTIONS_PROVIDED)

    def __build_firmware_uri(self, filename):
        return '/rest/firmware-drivers/' + filename


def main():
    SasLogicalInterconnectModule().run()


if __name__ == '__main__':
    main()
