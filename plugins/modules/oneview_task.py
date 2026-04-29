#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021-2024, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
module: oneview_task
short_description: Retrieve facts about the OneView Tasks.
description:
    - Retrieve facts about the OneView Tasks.
version_added: "2.4.0"
requirements:
    - "python >= 3.4.0"
    - "hpeOneView >= 6.1.0"
    - "ansible >= 2.9.0"
author: "Yuvarani Chidambaram (@yuvirani)"
options:
    sessionID:
       description:
         - Session ID to use for login to the appliance
       type: str
       required: false
    data:
       description: Get the tasks with state Running
       required: True
       type: dict
extends_documentation_fragment:
    - hpe.oneview.oneview
    - hpe.oneview.oneview.validateetag
    - hpe.oneview.oneview.params
'''

EXAMPLES = '''
tasks:
  - name: Gather facts about the last 5 running tasks
    oneview_task_facts:
    config: "{{ config }}"
    params:
      count: 5
      view: "tree"
      filter: ["taskState='Running'", "isCancellable=true"]
    delegate_to: localhost

  - debug: var=tasks

  - name: Sets the state of task to 'Cancelling'
    oneview_task:
    config: "{{ config }}"
    data:
      name: "{{ tasks[0]['name'] }}"
      uri: "{{ tasks[0]['uri'] }}"
    delegate_to: localhost
    when: contents.api_version >= 1200 and ( tasks | length > 0 )
'''

RETURN = '''
tasks:
    description: The updated task.
    returned: Always, but can be null.
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule, OneViewModuleException


class TaskModule(OneViewModule):
    MSG_TASK_UPDATED = 'Task has been updated.'
    MSG_RESOURCE_NOT_FOUND = 'Task Resource not found.'

    def __init__(self):
        argument_spec = dict(
            sessionID=dict(required=False, type='str'),
            data=dict(required=True, type='dict')
        )

        super(TaskModule, self).__init__(additional_arg_spec=argument_spec, validate_etag_support=True)

        self.set_resource_object(self.oneview_client.tasks)

    def execute_module(self):
        if not self.current_resource:
            return dict(failed=True,
                        msg=self.MSG_RESOURCE_NOT_FOUND)

        try:
            self.current_resource.patch(self.data['uri'])
        except OneViewModuleException as exception:
            error_msg = '; '.join(str(e) for e in exception.args)
            raise OneViewModuleException(error_msg)

        if not self.module.params.get("sessionID"):
            self.oneview_client.connection.logout()

        return dict(
            changed=True,
            msg=self.MSG_TASK_UPDATED,
            ansible_facts=dict(tasks=self.current_resource.data))


def main():
    TaskModule().run()


if __name__ == '__main__':
    main()
