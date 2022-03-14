#!/usr/bin/python
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
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_firmware_bundle
short_description: Provides an interface to Upload Firmware Bundle resources.
version_added: "2.9.0"
description:
    - Provides an interface to upload Firmware Bundle resources.
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 6.3.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    state:
        description:
            - Indicates the desired state for the Firmware Driver resource.
              C(present) will ensure that the hotfix/firmware bundle is at OneView.
              C(add_signature) will add the compsig to the hotfix/firmware bundle in OneView.
        choices: ['present', 'add_signature']
        required: True
        type: str
    file_path:
      description:
        - The full path of a local file to be uploaded.
      required: True
      type: str

extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Upload the Firmware Bundle
  oneview_firmware_bundle:
    config: "{{ config_file_path }}"
    state: present
    file_path: "/home/user/Downloads/hp-firmware.rpm"

- name: Upload the hotfix file
  oneview_firmware_bundle:
    config: "{{ config_file_path }}"
    state: present
    file_path: "/home/user/Downloads/hp-hotfix.zip"

- name: Add the compsig file
  oneview_firmware_bundle:
    config: "{{ config_file_path }}"
    state: add_signature
    file_path: "/home/user/Downloads/hp-hotfix.compsig"
'''

RETURN = '''
firmware_bundle:
    description: Has the facts about the OneView firmware bundle.
    returned: On state 'present'. Can be null.
    type: dict

compsig:
    description: Has the facts about the signature of OneView firmware bundle.
    returned: On state 'add_signature'.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule
import os.path


class FirmwareBundleModule(OneViewModule):
    MSG_ADDED = 'Firmware Bundle or Hotfix added successfully.'
    MSG_ALREADY_PRESENT = 'Firmware Bundle or Hotfix is already present.'
    MSG_ADD_SIG = 'Added the compsig successfully.'
    MSG_SIG_ALREADY_PRESENT = 'Signature already present.'
    MSG_HOTFIX_ABSENT = 'Hotfix is not present.'
    RESOURCE_FACT_NAME = 'firmware_bundle'

    def __init__(self):
        argument_spec = dict(state=dict(required=True, choices=['present', 'add_signature']),
                             file_path=dict(required=True, type='str'))

        super().__init__(additional_arg_spec=argument_spec, validate_etag_support=True)
        self.resource_client = self.oneview_client.firmware_bundles

    def execute_module(self):
        file_path = self.module.params['file_path']
        self.current_resource = self.resource_client.get_by_name(file_path)

        if self.state == 'present':
            return self.__present(file_path)
        elif self.state == 'add_signature':
            return self.__add_compsig(file_path)

    def __present(self, file_path):
        if not self.current_resource:
            self.current_resource = self.resource_client.upload(file_path)
            return dict(changed=True, msg=self.MSG_ADDED, ansible_facts=dict(firmware_bundle=self.current_resource))
        else:
            return dict(changed=False, msg=self.MSG_ALREADY_PRESENT, ansible_facts=dict(firmware_bundle=self.current_resource.data))

    def __add_compsig(self, file_path):
        file_name = basename(file_path)

        if self.current_resource and self.current_resource.data.get('resourceState') == 'AddFailed' and\
                self.current_resource.data.get('signatureFileRequired') is False:

            self.current_resource = self.resource_client.upload_compsig(
                file_path)
            return dict(changed=True, msg=self.MSG_ADD_SIG, ansible_facts=dict(compsig=self.current_resource))

        elif self.current_resource and self.current_resource.data.get('resourceState') == 'AddFailed' and\
                file_name not in self.current_resource.data.get('signatureFileName'):

            self.current_resource = self.resource_client.upload_compsig(
                file_path)
            return dict(changed=True, msg=self.MSG_ADD_SIG, ansible_facts=dict(compsig=self.current_resource))

        elif self.current_resource and self.current_resource.data.get('resourceState') == 'AddFailed' and\
                file_name in self.current_resource.data.get('signatureFileName'):
            return dict(changed=False, msg=self.MSG_SIG_ALREADY_PRESENT)

        elif self.current_resource and self.current_resource.data.get('signatureFileRequired') is True and\
                self.current_resource.data.get('resourceState') == 'Created':
            return dict(changed=False, msg=self.MSG_SIG_ALREADY_PRESENT)
        else:
            return dict(failed=True, msg=self.MSG_HOTFIX_ABSENT)


def main():
    FirmwareBundleModule().run()


if __name__ == '__main__':
    main()
