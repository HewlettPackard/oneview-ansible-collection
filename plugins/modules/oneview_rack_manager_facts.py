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
---

'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule


class RackManagerFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            uri=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
            sessionID=dict(required=False, type='str'),
        )
        super().__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.oneview_client.rack_managers)

    def execute_module(self):
        ansible_facts = {}
        rack_managers = []

        if self.module.params.get('name') or self.module.params.get('uri'):
            if self.current_resource:
                rack_managers = self.current_resource.data
                if self.options:
                    ansible_facts = self.gather_option_facts()
        else:
            if self.options and self.options.get('chassis'):
                ansible_facts['all_chassis'] = self.oneview_client.rack_managers.get_all_chassis()
            if self.options and self.options.get('managers'):
                ansible_facts['all_managers'] = self.oneview_client.rack_managers.get_all_managers()
            if self.options and self.options.get('partitions'):
                ansible_facts['all_partitions'] = self.oneview_client.rack_managers.get_all_partitions()

            rack_managers = self.resource_client.get_all(**self.facts_params)

        ansible_facts["rack_managers"] = rack_managers

        return dict(changed=False, ansible_facts=ansible_facts)

    def gather_option_facts(self):
        ansible_facts = {}

        if self.options.get('chassis'):
            ansible_facts['rack_manager_chassis'] = self.current_resource.get_associated_chassis()

        if self.options.get('partitions'):
            ansible_facts['rack_manager_partitions'] = self.current_resource.get_associated_partitions()

        if self.options.get('managers'):
            ansible_facts['rack_manager_managers'] = self.current_resource.get_associated_managers()

        if self.options.get('environmental_configuration'):
            ansible_facts['rack_manager_env_conf'] = self.current_resource.get_environmental_configuration()

        if self.options.get('remote_support_settings'):
            ansible_facts['rack_manager_remote_support'] = self.current_resource.get_remote_support_settings() 

        return ansible_facts

def main():
    RackManagerFactsModule().run()


if __name__ == '__main__':
    main()