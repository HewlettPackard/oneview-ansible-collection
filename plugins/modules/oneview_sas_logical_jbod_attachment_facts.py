#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2023-2024) Hewlett Packard Enterprise Development LP
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
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_sas_logical_jbod_attachment_facts
short_description: Retrieve facts about one or more SAS Logical JBOD Attachments
description:
    - Retrieve facts about one or more SAS Logical JBOD Attchments from OneView.
version_added: "2.5.0"
requirements:
    - hpeOneView >= 5.4.0
author:
    - Alisha K (@alisha-k-kalladassery)
options:
    name:
      description:
        - SAS Logical JBOD Attachment name
      type: str
    uri:
      description:
        - SAS Logical JBOD Attachment uri
      type: str
    sessionID:
      description:
        - Session ID to use for login to the appliance
      type: str
      required: false

extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.params
    - hpe.oneview.oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical JBOD Attachments
  oneview_sas_logical_jbod_attachment_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
  delegate_to: localhost

- debug: var=sas_logical_jbod_attachments

- set_fact:
    jbod_attachment_name: "{{ sas_logical_jbod_attachments[0]['name'] }}"
- set_fact:
    jbod_attachment_uri: "{{ sas_logical_jbod_attachments[0]['uri'] }}"

- name: Gather paginated, filtered and sorted facts about SAS Logical JBOD attachments
  oneview_sas_logical_jbod_attachment_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=sas_logical_jbod_attachments

- name: Gather facts about a SAS Logical JBOD Attachment by name
  oneview_sas_logical_jbod_attachment_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    name: "{{ jbod_attachment_name }}"
  delegate_to: localhost

- debug: var=sas_logical_jbod_attachments

- name: Gather facts about a SAS Logical JBOD Attachment by uri
  oneview_sas_logical_jbod_attachment_facts:
    hostname: 1.2.3.4
    username: administrator
    password: my_password
    api_version: 4600
    uri: "{{ jbod_attachment_uri }}"
  delegate_to: localhost

- debug: var=sas_logical_jbod_attachments
'''

RETURN = '''
sas_logical_jbod_attachments:
    description: Has all the OneView facts about the SAS logical JBOD attachments.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class SasLogicalJbodAttachmentFactsModule(OneViewModule):
    argument_spec = dict(name=dict(type='str'), uri=dict(required=False, type='str'), sessionID=dict(required=False, type='str'), params=dict(type='dict'))

    def __init__(self):
        super().__init__(additional_arg_spec=self.argument_spec, supports_check_mode=True)
        self.set_resource_object(self.oneview_client.sas_logical_jbod_attachments)

    def execute_module(self):

        ansible_facts = {}

        if self.current_resource:
            sas_logical_jbod_attachments = [self.current_resource.data]
        elif not self.module.params.get("name") and not self.module.params.get('uri'):
            sas_logical_jbod_attachments = self.resource_client.get_all(**self.facts_params)
        else:
            sas_logical_jbod_attachments = []

        ansible_facts['sas_logical_jbod_attachments'] = sas_logical_jbod_attachments

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(changed=False,
                    ansible_facts=ansible_facts)


def main():
    SasLogicalJbodAttachmentFactsModule().run()


if __name__ == '__main__':
    main()
