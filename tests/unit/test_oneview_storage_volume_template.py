#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import StorageVolumeTemplateModule

FAKE_MSG_ERROR = 'Fake message error'

STORAGE_VOLUME_TEMPLATE = dict(
    name='StorageVolumeTemplate Test',
    state='Configured',
    description='Example Template',
    provisioning=dict(
        shareable='true',
        provisionType='Thin',
        capacity='235834383322',
        storagePoolUri='{{storage_pool_uri}}'),
    stateReason='None',
    storageSystemUri='{{ storage_system_uri }}',
    snapshotPoolUri='{{storage_pool_uri}}',
    type='StorageVolumeTemplateV3'
)

STORAGE_VOLUME_TEMPLATE_WITH_NEW_DESCRIPTION = dict(
    STORAGE_VOLUME_TEMPLATE, description='Example Template with a new description')

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=STORAGE_VOLUME_TEMPLATE
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=STORAGE_VOLUME_TEMPLATE_WITH_NEW_DESCRIPTION
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=STORAGE_VOLUME_TEMPLATE['name'])
)

PARAMS_FOR_MISSING_KEY = dict(
    config='config.json',
    state='present',
    data=dict(state='Configured')
)


@pytest.mark.resource(TestStorageVolumeTemplateModule='storage_volume_templates')
class TestStorageVolumeTemplateModule(OneViewBaseTest):
    def test_should_create_new_storage_volume_template(self):
        self.resource.get_by_name.return_value = None
        obj = mock.Mock()
        obj.data = {"name": "name"}
        self.resource.create.return_value = obj

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageVolumeTemplateModule.MSG_CREATED,
            ansible_facts=dict(storage_volume_template={"name": "name"})
        )

    def test_should_update_the_storage_volume_template(self):
        obj = mock.Mock()
        obj.data = STORAGE_VOLUME_TEMPLATE
        self.resource.get_by_name.return_value = obj
        obj = mock.Mock()
        obj.data = {"name": "name"}
        self.resource.update.return_value = obj

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageVolumeTemplateModule.MSG_UPDATED,
            ansible_facts=dict(storage_volume_template=STORAGE_VOLUME_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        obj = mock.Mock()
        obj.data = STORAGE_VOLUME_TEMPLATE
        self.resource.get_by_name.return_value = obj

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StorageVolumeTemplateModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(storage_volume_template=STORAGE_VOLUME_TEMPLATE)
        )

    def test_should_remove_storage_volume_template(self):
        obj = mock.Mock()
        obj.data = STORAGE_VOLUME_TEMPLATE
        self.resource.get_by_name.return_value = obj

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageVolumeTemplateModule.MSG_DELETED
        )

    def test_should_do_nothing_when_storage_volume_template_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StorageVolumeTemplateModule.MSG_ALREADY_ABSENT
        )

    def test_should_raise_exception_when_key_is_missing(self):
        obj = mock.Mock()
        obj.data = STORAGE_VOLUME_TEMPLATE
        self.resource.get_by_name.return_value = obj

        self.resource.remove.side_effect = Exception(FAKE_MSG_ERROR)

        self.mock_ansible_module.params = PARAMS_FOR_MISSING_KEY

        StorageVolumeTemplateModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=StorageVolumeTemplateModule.MSG_MANDATORY_FIELD_MISSING)


if __name__ == '__main__':
    pytest.main([__file__])
