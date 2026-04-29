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
module: oneview_certificates_server
short_description: Manage OneView Server Certificate resources.
description:
    - Provides an interface to manage Server Certificate resources. Can create, update, and delete.
version_added: "2.4.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.4.0"
author: "Venkatesh Ravula (@VenkateshRavula)"
options:
    sessionID:
        description:
          - Session ID to use for login to the appliance
        type: str
        required: false
    state:
        description:
            - Indicates the desired state for the Server Certificate resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
        type: str
    name:
        description:
            - Indicates the alias name of the certificates server resource.
        required: true
        type: str
    data:
        description:
            - List with the Server Certificate properties.
        required: true
        type: dict
extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Create a Server Certificate
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    name: "172.18.13.11"
    data:
      certificateDetails:
        - aliasName: 'vcenter'
          base64Data: '--- Certificate ---'
- name: Update the Server Certificate name to 'vcenter Renamed'
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: present
    name: "172.18.13.11"
    data:
      name: 'vcenter renamed'
      certificateDetails:
        - aliasName: 'vcenter'
          base64Data: '--- Certificate ---'
- name: Ensure that the Hypervisor Manager is absent
  oneview_certificates_server:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    state: absent
    name: "172.18.13.11"
    data:
      alias_name: 'vcenter'
'''

RETURN = '''
certificate_server:
    description: Has the facts about the managed OneView Hypervisor Manager.
    returned: On state 'present'. Can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class CertificatesServerModule(OneViewModule):
    MSG_CREATED = 'Server Certificate created successfully.'
    MSG_UPDATED = 'Server Certificate updated successfully.'
    MSG_DELETED = 'Server Certificate deleted successfully.'
    MSG_ALREADY_PRESENT = 'Server Certificate is already present.'
    MSG_ALREADY_ABSENT = 'Server Certificate is already absent.'
    RESOURCE_FACT_NAME = 'certificate_server'

    def __init__(self):
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   name=dict(required=True, type='str'),
                                   sessionID=dict(required=False, type='str'),
                                   state=dict(
                                       required=True,
                                       choices=['present', 'absent']))

        super().__init__(additional_arg_spec=additional_arg_spec,
                         validate_etag_support=True)
        self.__set_current_resource(self.oneview_client.certificates_server)

    def execute_module(self):
        result = {}
        if self.state == 'present':
            result = self.resource_present(self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            result = self.resource_absent()
        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()
        return result

    def __set_current_resource(self, resource_client):
        self.resource_client = resource_client
        aliasname = None

        if self.module.params.get('name'):
            aliasname = self.module.params['name']

        if self.resource_client.get_by_alias_name(aliasname):
            self.current_resource = self.resource_client.get_by_alias_name(aliasname)


def main():
    CertificatesServerModule().run()


if __name__ == '__main__':
    main()
