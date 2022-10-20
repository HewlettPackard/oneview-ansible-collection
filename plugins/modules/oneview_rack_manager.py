#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2022) Hewlett Packard Enterprise Development LP
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
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (OneViewModule, OneViewModuleResourceNotFound,
                                                                          OneViewModuleValueError)


class RackManagerModule(OneViewModule):
    MSG_ADDED = 'Rack Manager added successfully.'
    MSG_ALREADY_PRESENT = 'Rack Manager is already present.'
    MSG_DELETED = 'Rack Manager deleted successfully.'
    MSG_ALREADY_ABSENT = 'Rack Manager is already absent.'
    MSG_RACK_MANAGER_REFRESHED = 'Rack Manager refreshed successfully.'
    MSG_RACK_MANAGER_NOT_FOUND = 'The provided rack manager was not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=[
                'present',
                'absent',
                'refresh_state_set'
            ]
        ),
        sessionID=dict(required=False, type='str'),
        data=dict(required=True, type='dict')
    )

    def __init__(self):

        super().__init__(additional_arg_spec=self.argument_spec, validate_etag_support=True)
        self.set_resource_object(self.oneview_client.rack_managers)

    def execute_module(self):

        if self.state == 'present':
            return self.__present()
        else:
            if not self.data.get('name'):
                raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.name"))

            if self.state == 'absent':
                return self.resource_absent(method='remove')
            else:
                if not self.current_resource:
                    raise OneViewModuleResourceNotFound(self.MSG_RACK_MANAGER_NOT_FOUND)
                else:
                    if self.state == 'refresh_state_set':
                        self.current_resource.patch('RefreshRackManagerOp','','')
                        return dict(changed=True,
                                    msg=self.MSG_RACK_MANAGER_REFRESHED,
                                    ansible_facts=dict(rack_manager=self.current_resource.data))

    def __present(self):

        if not self.data.get('hostname'):
            raise OneViewModuleValueError(self.MSG_MANDATORY_FIELD_MISSING.format("data.hostname"))

        self.current_resource = self.resource_client.get_by_name(self.data['hostname'])

        result = dict()

        if not self.current_resource:
            self.current_resource = self.resource_client.add(self.data)
            result = dict(
                changed=True,
                msg=self.MSG_ADDED,
                ansible_facts={'rack_manager': self.current_resource.data}
            )
        else:
            result = dict(
                changed=False,
                msg=self.MSG_ALREADY_PRESENT,
                ansible_facts={'rack_manager': self.current_resource.data}
            )
        return result


def main():
    RackManagerModule().run()


if __name__ == '__main__':
    main()