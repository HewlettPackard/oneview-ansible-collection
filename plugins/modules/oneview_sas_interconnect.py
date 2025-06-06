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
module: oneview_sas_interconnect
short_description: Manage OneView SAS Interconnect resources.
description:
    - Provides an interface to manage SAS Interconnect resources.
version_added: "2.3.0"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.4.0"
author: "Alisha K (@alisha-k-kalladassery)"
options:
    sessionID:
      description:
        - Session ID to use for login to the appliance
      type: str
      required: false
    state:
      description:
        - Indicates the desired state for the SAS Interconnect resource.
          C(refreshed) will refresh the sas interconnect.
          C(power_on) will power on the sas interconnect.
          C(power_off) will power off the sas interconnect.
          C(uid_on) will set the UID state On.
          C(uid_off) will set the UID state Off.
          C(hard_reset) Request a hard reset of the sas interconnect. A hard reset will interrupt active I/O.
          C(soft_reset) Request a soft reset of the interconnect. A soft reset will reset the management processor and will not disrupt I/O.
      choices: [
        'refreshed', 'power_on', 'power_off', 'uid_on', 'uid_off', 'hard_reset', 'soft_reset'
        ]
      type: str
      required: true
    validate_etag:
      description:
         - When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag
           for the resource matches the ETag provided in the data.
      default: true
      choices: []
      type: bool
    data:
      description:
        - List with the SAS Interconnect properties.
      required: true
      type: dict
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
---
- name: Fetch Session Id
  oneview_get_session_id:
    config: "{{ config }}"
    name: "Test_Session"
  delegate_to: localhost
  register: session

- debug: var=session

- name: Gather facts about all SAS Interconnects
  oneview_sas_interconnect_facts:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
  delegate_to: localhost

- set_fact:
    variant: "Synergy"
- set_fact:
    sas_interconnect_name: "{{ sas_interconnects[0]['name'] }}"

- name: Refresh the SAS interconnect
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: refreshed
    data:
      name: '{{ sas_interconnect_name }}'
      refreshState: 'RefreshPending'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Power Off the SAS interconnect
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: power_off
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Do nothing when SAS interconnect is already powered off
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: power_off
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Power On the SAS interconnect
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: power_on
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Do nothing when SAS interconnect is already powered on
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: power_on
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Set the UID state of the SAS interconnect to On
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: uid_on
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Do nothing when UID state is already set to On
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: uid_on
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Set the UID state of the SAS interconnect to Off
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: uid_off
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Do nothing when UID state is already set to Off
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: uid_off
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Request a hard reset of the SAS interconnect
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: hard_reset
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'

- name: Request a soft reset of the SAS interconnect
  oneview_sas_interconnect:
    config: "{{ config }}"
    sessionID: "{{ session.ansible_facts.session }}"
    state: soft_reset
    data:
      name: '{{ sas_interconnect_name }}'
  when: variant == 'Synergy'
  delegate_to: localhost
  register: result
- debug: var=result.msg
  when: variant == 'Synergy'
'''

RETURN = '''
sas_interconnect:
    description: Has all the facts about the sas interconnect.
    returned: On states 'refreshed', 'power_on', 'power_off', 'uid_on', 'uid_off' 'soft_reset' and 'hard_reset'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (OneViewModule, OneViewModuleResourceNotFound, OneViewModuleValueError)


class SasInterconnectModule(OneViewModule):
    MSG_SAS_INTERCONNECT_REFRESHED = "SAS Interconnect refreshed successfully."
    MSG_SAS_INTERCONNECT_POWERED_ON = "SAS Interconnect is powered On successfully."
    MSG_SAS_INTERCONNECT_ALREADY_POWERED_ON = "SAS Interconnect is already powered On."
    MSG_SAS_INTERCONNECT_POWERED_OFF = "SAS Interconnect is powered Off successfully."
    MSG_SAS_INTERCONNECT_ALREADY_POWERED_OFF = "SAS Interconnect is already powered Off."
    MSG_UID_POWERED_ON = "UID state set to On successfully."
    MSG_UID_ALREADY_POWERED_ON = "UID state is already set to On."
    MSG_UID_POWERED_OFF = "UID state set to Off successfully."
    MSG_UID_ALREADY_POWERED_OFF = "UID state is already set to Off."
    MSG_HARD_RESET_SAS_INTERCONNECT = "Hard Reset SAS Interconnect successfully."
    MSG_SOFT_RESET_SAS_INTERCONNECT = "Soft Reset SAS Interconnect successfully."
    MSG_SAS_INTERCONNECT_NOT_FOUND = "SAS Interconnect not found."
    MSG_SAS_INTERCONNECT_NAME_REQUIRED = "SAS Interconnect name is required."

    argument_spec = dict(
        state=dict(
            required=True,
            choices=[
                'refreshed',
                'power_on',
                'power_off',
                'uid_on',
                'uid_off',
                'hard_reset',
                'soft_reset'
            ]
        ),
        sessionID=dict(required=False, type='str'),
        data=dict(required=True, type='dict')
    )
    patch_params = dict(
        power_on=dict(operation='replace', path='/powerState', value='On'),
        power_off=dict(operation='replace', path='/powerState', value='Off'),
        uid_on=dict(operation='replace', path='/uidState', value='On'),
        uid_off=dict(operation='replace', path='/uidState', value='Off'),
        hard_reset=dict(operation='replace', path='/hardResetState', value='Reset'),
        soft_reset=dict(operation='replace', path='/softResetState', value='Reset')
    )

    patch_messages = dict(
        power_on=dict(changed=MSG_SAS_INTERCONNECT_POWERED_ON, not_changed=MSG_SAS_INTERCONNECT_ALREADY_POWERED_ON),
        power_off=dict(changed=MSG_SAS_INTERCONNECT_POWERED_OFF, not_changed=MSG_SAS_INTERCONNECT_ALREADY_POWERED_OFF),
        uid_on=dict(changed=MSG_UID_POWERED_ON, not_changed=MSG_UID_ALREADY_POWERED_ON),
        uid_off=dict(changed=MSG_UID_POWERED_OFF, not_changed=MSG_UID_ALREADY_POWERED_OFF),
        hard_reset=dict(changed=MSG_HARD_RESET_SAS_INTERCONNECT),
        soft_reset=dict(changed=MSG_SOFT_RESET_SAS_INTERCONNECT)
    )

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.sas_interconnects)

    def execute_module(self):
        if not self.data.get("name"):
            raise OneViewModuleValueError(self.MSG_SAS_INTERCONNECT_NAME_REQUIRED)
        if not self.current_resource:
            raise OneViewModuleResourceNotFound(self.MSG_SAS_INTERCONNECT_NOT_FOUND)
        else:
            if self.state == 'refreshed':
                changed, msg, resource = self.__refresh()
            else:
                changed, msg, resource = self.__patch(self.state)

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(sas_interconnects=resource))

    def __refresh(self):
        refresh_config = self.data.copy()
        refresh_config.pop('name', None)

        self.current_resource.refresh_state(refresh_config)

        return True, self.MSG_SAS_INTERCONNECT_REFRESHED, self.current_resource.data

    def __patch(self, state):
        changed = False
        state_name = self.module.params['state']
        state = self.patch_params[state_name].copy()
        current_property_value = self.__get_current_property_value(state)

        if current_property_value and self.__is_update_needed(state_name, state, current_property_value):
            resource_obj = self.current_resource.patch(**state)
            resource = resource_obj.data
            changed = True
        else:
            resource = self.current_resource.data

        msg = self.patch_messages[state_name]['changed'] if changed else self.patch_messages[state_name]['not_changed']

        return changed, msg, resource

    def __get_current_property_value(self, state):
        property_name = state['path'].split('/')[1]
        if self.current_resource.data.get(property_name):
            return self.current_resource.data.get(property_name)
        else:
            return None

    def __is_update_needed(self, state_name, state, current_property_value):
        need_request_update = False
        if (state_name == 'hardResetState' or state_name == 'softResetState'):
            need_request_update = True
        elif current_property_value != state['value']:
            need_request_update = True
        return need_request_update


def main():
    SasInterconnectModule().run()


if __name__ == '__main__':
    main()
