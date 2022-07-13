#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2021) Hewlett Packard Enterprise Development LP
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

from copy import deepcopy
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import VolumeModule

FAKE_MSG_ERROR = 'Fake message error'

volume_template = dict(
    name='vol-temp',
    uri='/rest/storage-volume-templates/3B1CF17F-7657-4C89-B580-D236507A9182',
    properties=dict(
        size=dict(default=102400),
        storagePool=dict(default='/rest/storage-pools/1')
    )
)

EXISTENT_VOLUME = dict(
    name='Volume with Storage Pool',
    description='Test volume with common creation: Storage Pool',
    uri='/rest/storage-volumes/3B1CF17F-7657-4C89-B580-D236507A9182'
)

EXISTENT_VOLUME_WITH_NEW_NAME = dict(
    name='Volume with Storage Pool - Renamed',
    description='Test volume with common creation: Storage Pool',
    uri='/rest/storage-volumes/F28FC559-0896-4D14-A694-DB70C784BB9E'
)

SNAPSHOT_URI = EXISTENT_VOLUME['uri'] + '/snapshots/CA9E652A-A45A-45DA-BD2A-1A7638BF1699'

PARAMS_FOR_CREATE = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool',
              provisioningParameters=dict(provisionType='Full',
                                          shareable=True,
                                          requestedCapacity=1073741824,
                                          storagePoolUri='/rest/storage-pools/3B1CF17F-7657-4C89-B580-D236507A9182'))
)

PARAMS_FOR_CREATE_WITH_TEMPLATE_NAME = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage template',
              templateName='vol-temp',
              properties=dict(provisionType='Full',
                              shareable=True)
              )
)

PARAMS_FOR_CREATE_FROM_SNAPSHOT = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool',
              snapshotUri='/rest/snapshot/fake'))

PARAMS_FOR_MANAGED = dict(
    config='config.json',
    state='managed',
    data=dict(deviceVolumeName='Volume with Storage Pool'))

PARAMS_FOR_PROPERTY_NAME = dict(
    config='config.json',
    state='present',
    data=dict(properties=dict(name='Volume with Storage Pool')))

PARAMS_FOR_UPDATE_template = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool',
              templateUri='/rest/fake')
)

PARAMS_FOR_UPDATE_OK = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool',
              newName='NEWNAME',
              shareable=False)
)

PARAMS_FOR_UPDATE_EXISTING = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool',
              newName='Volume with Storage Pool - Renamed',
              shareable=False)
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name='Volume with Storage Pool')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name='Volume with Storage Pool')
)

PARAMS_FOR_ABSENT_EXPORT_ONLY = dict(
    config='config.json',
    state='absent',
    data=dict(name='Volume with Storage Pool'),
    export_only=True
)

PARAMS_FOR_ABSENT_SUPPRESS = dict(
    config='config.json',
    state='absent',
    data=dict(name='Volume with Storage Pool'),
    suppress_device_updates=True
)

PARAMS_FOR_REPAIR = dict(
    config='config.json',
    state='repaired',
    data=dict(name='Volume with Storage Pool')
)

PARAMS_FOR_SNAPSHOT_CREATED = dict(
    config='config.json',
    state='snapshot_created',
    data=dict(name='Volume with Storage Pool',
              snapshotParameters=dict(name='filename',
                                      type='Snapshot'))
)

PARAMS_FOR_SNAPSHOT_DELETED = dict(
    config='config.json',
    state='snapshot_deleted',
    data=dict(name='Volume with Storage Pool',
              snapshotParameters=dict(name='filename',
                                      type='Snapshot'))
)


@pytest.mark.resource(TestVolumeModule='volumes')
class TestVolumeModule(OneViewBaseTest):
    def test_should_raise_error_volume_with_template_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ov_client.storage_volume_templates.get_by_name.return_value = None

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_CREATE_WITH_TEMPLATE_NAME)

        VolumeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=VolumeModule.MSG_TEMPLATE_NOT_FOUND.format("vol-temp"))

    def test_should_create_new_volume_when_not_exist(self):
        self.resource.get_by_name.return_value = []
        self.resource.create.return_value = self.resource
        self.resource.data = EXISTENT_VOLUME

        self.mock_ansible_module.params = PARAMS_FOR_CREATE

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_CREATED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME)
        )

    def test_should_create_new_volume_with_template_name(self):
        self.resource.get_by_name.return_value = None
        self.mock_ov_client.storage_volume_templates.data = volume_template
        self.mock_ov_client.storage_volume_templates.get_by_name.return_value = self.mock_ov_client.storage_volume_templates

        self.resource.data = EXISTENT_VOLUME
        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = deepcopy(PARAMS_FOR_CREATE_WITH_TEMPLATE_NAME)

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_CREATED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME)
        )

    def test_should_find_from_name_in_properties(self):
        self.resource.data = {"name": "Volume with Storage Pool"}
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PROPERTY_NAME

        VolumeModule().run()

        self.resource.get_by_name.assert_called_once_with("Volume with Storage Pool")

    def test_should_create_from_snapshot(self):
        self.resource.get_by_name.return_value = []
        self.resource.create_from_snapshot.return_value = self.resource
        self.resource.data = EXISTENT_VOLUME

        self.mock_ansible_module.params = PARAMS_FOR_CREATE_FROM_SNAPSHOT

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_CREATED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME)
        )

    def test_should_add_for_management(self):
        self.resource.get_by_name.return_value = None
        self.resource.add_from_existing.return_value = EXISTENT_VOLUME

        self.mock_ansible_module.params = PARAMS_FOR_MANAGED

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_ADDED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME)
        )

    def test_should_not_add_already_managed_volume(self):
        self.resource.data = EXISTENT_VOLUME
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_MANAGED

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=VolumeModule.MSG_ALREADY_MANAGED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME)
        )

    def test_should_update_volume_when_already_exist(self):
        self.resource.data = EXISTENT_VOLUME
        self.resource.get_by_name.side_effect = [self.resource, None]

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_OK

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_UPDATED,
            ansible_facts=dict(storage_volume=EXISTENT_VOLUME)
        )

    def test_should_raise_exception_when_new_name_already_used(self):
        self.resource.get_by.side_effect = [[EXISTENT_VOLUME], [EXISTENT_VOLUME_WITH_NEW_NAME]]

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_EXISTING

        VolumeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=VolumeModule.MSG_NEW_NAME_INVALID)

    def test_should_delete_volume(self):
        self.resource.data = EXISTENT_VOLUME
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        VolumeModule().run()

        self.resource.delete.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_DELETED
        )

    def test_should_remove_volume_with_export_only(self):
        self.resource.data = EXISTENT_VOLUME
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT_EXPORT_ONLY

        VolumeModule().run()

        self.resource.delete.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_DELETED
        )

    def test_should_remove_volume_with_suppress_device_updates(self):
        self.resource.data = EXISTENT_VOLUME
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT_SUPPRESS

        VolumeModule().run()

        self.resource.delete.assert_called_once_with()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_DELETED
        )

    def test_update_should_do_nothing_when_volume_already_exists_with_template(self):
        self.resource.data = PARAMS_FOR_PRESENT["data"]
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_UPDATE_template

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_UPDATED,
            ansible_facts=dict(storage_volume=self.resource.data)
        )

    def test_update_should_do_nothing_when_volume_already_exists_and_is_equal(self):
        self.resource.data = PARAMS_FOR_PRESENT["data"]
        self.resource.get_by_name.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=VolumeModule.MSG_NO_CHANGES_PROVIDED,
            ansible_facts=dict(storage_volume=self.resource.data)
        )

    def test_should_do_nothing_when_volume_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=VolumeModule.MSG_ALREADY_ABSENT
        )

    def test_should_repair_volume(self):
        self.resource.get_by.return_value = [EXISTENT_VOLUME]

        self.mock_ansible_module.params = PARAMS_FOR_REPAIR

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_REPAIRED
        )

    def test_should_create_snapshot(self):
        self.resource.get_by.return_value = [EXISTENT_VOLUME]

        self.mock_ansible_module.params = PARAMS_FOR_SNAPSHOT_CREATED

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_SNAPSHOT_CREATED
        )

    def test_should_not_create_snapshot_when_resource_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_SNAPSHOT_CREATED

        VolumeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=VolumeModule.MSG_NOT_FOUND)

    def test_should_fail_when_is_missing_data_attributes_on_snapshot_creation(self):
        self.resource.get_by.return_value = [EXISTENT_VOLUME]

        params = deepcopy(PARAMS_FOR_SNAPSHOT_CREATED)
        del params['data']['snapshotParameters']

        self.mock_ansible_module.params = params

        VolumeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=VolumeModule.MSG_NO_OPTIONS_PROVIDED)

    def test_should_delete_snapshot(self):
        self.resource.get_by.return_value = [EXISTENT_VOLUME]
        self.resource.get_snapshot_by.return_value = [{'uri': SNAPSHOT_URI}]

        self.mock_ansible_module.params = PARAMS_FOR_SNAPSHOT_DELETED

        VolumeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=VolumeModule.MSG_SNAPSHOT_DELETED
        )

    def test_should_fail_when_is_missing_data_attributes_on_snapshot_deletion(self):
        self.resource.get_by.return_value = [EXISTENT_VOLUME]
        self.resource.get_snapshot_by.return_value = [{'uri': SNAPSHOT_URI}]

        params = deepcopy(PARAMS_FOR_SNAPSHOT_DELETED)
        del params['data']['snapshotParameters']

        self.mock_ansible_module.params = params

        VolumeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=VolumeModule.MSG_NO_OPTIONS_PROVIDED)

    def test_should_not_delete_snapshot_when_resource_not_exist(self):
        self.resource.get_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_SNAPSHOT_DELETED

        VolumeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=VolumeModule.MSG_NOT_FOUND)

    def test_should_not_delete_snapshot_when_snapshot_not_exist(self):
        self.resource.get_by.return_value = [EXISTENT_VOLUME]
        self.resource.get_snapshot_by_name.return_value = None

        self.mock_ansible_module.params = PARAMS_FOR_SNAPSHOT_DELETED

        VolumeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=VolumeModule.MSG_SNAPSHOT_NOT_FOUND)


if __name__ == '__main__':
    pytest.main([__file__])
