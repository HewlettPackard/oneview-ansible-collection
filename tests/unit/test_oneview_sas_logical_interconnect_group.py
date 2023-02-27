#!/usr/bin/env python
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

import mock
import pytest
import yaml

from copy import deepcopy
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import SasLogicalInterconnectGroupModule

SAS_LIG_FROM_ONEVIEW = dict(
    name="SAS_LIG",
    enclosureType='SY12000',
    interconnectMapTemplate=dict(
        interconnectMapEntryTemplates=[dict(
            enclosureIndex=1,
            logicalLocation=dict(locationEntries=[dict(
                relativeValue=1,
                type="Bay"
            ), dict(
                relativeValue=1,
                type="Enclosure"
            )
            ]),
            permittedInterconnectTypeUri="/rest/sas-interconnect-types/18c3a8d1-cb92-4e71-b9ad-224c9d289c03"
        )]
    )
)
PARAMS_FOR_CREATE = dict(
    config="config.json",
    state="present",
    data=dict(
        name="SAS_LIG",
        enclosureType="SY12000",
        interconnectMapTemplate=dict(
            interconnectMapEntryTemplates=[
                dict(
                    enclosureIndex=1,
                    logicalLocation=dict(
                        locationEntries=[
                            dict(relativeValue=1, type="Bay"),
                            dict(relativeValue=1, type="Enclosure"),
                        ]
                    ),
                    permittedInterconnectTypeUri="/rest/sas-interconnect-types/18c3a8d1-cb92-4e71-b9ad-224c9d289c03",
                )
            ]
        ),
    ),
)
PARAMS_FOR_CREATE_NO_NAME = dict(
    config="config.json",
    state="present",
    data=dict(
        enclosureType="SY12000",
        interconnectMapTemplate=dict(
            interconnectMapEntryTemplates=[
                dict(
                    enclosureIndex=1,
                    logicalLocation=dict(
                        locationEntries=[
                            dict(relativeValue=1, type="Bay"),
                            dict(relativeValue=1, type="Enclosure"),
                        ]
                    ),
                    permittedInterconnectTypeUri="/rest/sas-interconnect-types/18c3a8d1-cb92-4e71-b9ad-224c9d289c03",
                )
            ]
        ),
    ),
)
PARAMS_FOR_DELETE = dict(
    config='config.json',
    state='absent',
    data=dict(name='SAS_LIG')
)
PARAMS_FOR_NAME_CHANGE = dict(
    config='config.json',
    state='present',
    data=dict(name='SAS_LIG',
              newName="New_SAS_LIG")
)
PARAMS_FOR_UPDATE = dict(
    config="config.json",
    state="present",
    data=dict(
        name="SAS_LIG",
        enclosureType="SY12000",
        interconnectMapTemplate=dict(
            interconnectMapEntryTemplates=[
                dict(
                    enclosureIndex=1,
                    logicalLocation=dict(
                        locationEntries=[
                            dict(relativeValue=1, type="Bay"),
                            dict(relativeValue=1, type="Enclosure"),
                        ]
                    ),
                    permittedInterconnectTypeUri="/rest/sas-interconnect-types/18c3a8d1-cb92-4e71-b9ad",
                )
            ]
        ),
    ),
)
RESOURCE_AFTER_UPDATE = dict(
    name="SAS_LIG",
    enclosureType="SY12000",
    interconnectMapTemplate=dict(
        interconnectMapEntryTemplates=[
            dict(
                enclosureIndex=1,
                logicalLocation=dict(
                    locationEntries=[
                        dict(relativeValue=1, type="Bay"),
                        dict(relativeValue=1, type="Enclosure"),
                    ]
                ),
                permittedInterconnectTypeUri="/rest/sas-interconnect-types/18c3a8d1-cb92-4e71-b9ad",
            )
        ]
    ),
)
RESOURCE_AFTER_NAME_UPDATE = dict(
    name="New_SAS_LIG",
    enclosureType="SY12000",
    interconnectMapTemplate=dict(
        interconnectMapEntryTemplates=[
            dict(
                enclosureIndex=1,
                logicalLocation=dict(
                    locationEntries=[
                        dict(relativeValue=1, type="Bay"),
                        dict(relativeValue=1, type="Enclosure"),
                    ]
                ),
                permittedInterconnectTypeUri="/rest/sas-interconnect-types/18c3a8d1-cb92-4e71-b9ad-224c9d289c03",
            )
        ]
    ),
)


@pytest.mark.resource(TestSasLogicalInterconnectGroupModule='sas_logical_interconnect_groups')
class TestSasLogicalInterconnectGroupModule(OneViewBaseTest):
    def test_should_create_sas_lig(self):
        self.resource.get_by_name.return_value = None
        self.resource.data = SAS_LIG_FROM_ONEVIEW
        self.resource.create.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_CREATE

        SasLogicalInterconnectGroupModule().run()

        self.resource.create.assert_called_once_with(PARAMS_FOR_CREATE["data"])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_interconnect_group=SAS_LIG_FROM_ONEVIEW),
            msg=SasLogicalInterconnectGroupModule.MSG_CREATED
        )

    def test_should_not_create_if_sas_lig_exists(self):
        self.resource.data = SAS_LIG_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_CREATE

        SasLogicalInterconnectGroupModule().run()

        self.resource.create.not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnect_group=SAS_LIG_FROM_ONEVIEW),
            msg=SasLogicalInterconnectGroupModule.MSG_ALREADY_PRESENT
        )

    def test_should_update_sas_lig(self):
        self.resource.data = SAS_LIG_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.update.return_value.data = RESOURCE_AFTER_UPDATE
        self.mock_ansible_module.params = PARAMS_FOR_UPDATE

        SasLogicalInterconnectGroupModule().run()

        self.resource.update.assert_called_once_with(PARAMS_FOR_UPDATE["data"])

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_interconnect_group=self.resource.data),
            msg=SasLogicalInterconnectGroupModule.MSG_UPDATED
        )

    def test_should_not_update_on_same_data(self):
        self.resource.data = SAS_LIG_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_FOR_CREATE

        SasLogicalInterconnectGroupModule().run()

        self.resource.create.not_been_called()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_interconnect_group=SAS_LIG_FROM_ONEVIEW),
            msg=SasLogicalInterconnectGroupModule.MSG_ALREADY_PRESENT
        )

    def test_should_not_update_if_no_lig_found(self):
        self.resource.get_by_name.return_value = None
        self.mock_ansible_module.params = PARAMS_FOR_CREATE_NO_NAME

        SasLogicalInterconnectGroupModule().run()
        self.resource.create.not_been_called()

    def test_should_update_new_name(self):
        self.resource.data = SAS_LIG_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource
        self.resource.update.return_value.data = RESOURCE_AFTER_NAME_UPDATE
        self.mock_ansible_module.params = PARAMS_FOR_NAME_CHANGE

        SasLogicalInterconnectGroupModule().run()

        self.resource.update.assert_called_once_with(RESOURCE_AFTER_NAME_UPDATE)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(sas_logical_interconnect_group=self.resource.data),
            msg=SasLogicalInterconnectGroupModule.MSG_UPDATED
        )

    def test_should_remove_sas_lig(self):
        self.resource.data = SAS_LIG_FROM_ONEVIEW
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_DELETE

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectGroupModule.MSG_DELETED
        )

    def test_should_do_nothing_when_lig_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_DELETE

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasLogicalInterconnectGroupModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
