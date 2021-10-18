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
import yaml

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import StorageVolumeAttachmentModule

FAKE_MSG_ERROR = 'Fake message error'

SERVER_PROFILE_NAME = "SV-1001"

YAML_EXTRA_REMOVED_BY_NAME = """
        config: "{{ config }}"
        state: extra_presentations_removed
        server_profile: "SV-1001"
        """
YAML_EXTRA_REMOVED_BY_URI = """
        config: "{{ config }}"
        state: extra_presentations_removed
        server_profile: "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
        """

REPAIR_DATA = {
    "type": "ExtraUnmanagedStorageVolumes",
    "resourceUri": "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
}

MOCK_SERVER_PROFILE = {
    "affinity": "BayAndServer",
    "associatedServer": "SGH106X8RN",
    "name": "SV-1001",
    "uri": "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d",
    "sanStorage": {
        "manageSanStorage": True,
        "volumeAttachments": [
            {
                "id": 1,
                "lun": "1",
                "lunType": "Auto",
                "state": "AttachFailed",
                "storagePaths": [
                    {
                        "connectionId": 1,
                        "isEnabled": True,
                        "storageTargets": [
                            "20:00:00:02:AC:00:08:F7"
                        ]
                    }
                ],
                "volumeStoragePoolUri": "/rest/storage-pools/280FF951-F007-478F-AC29-E4655FC76DDC",
                "volumeStorageSystemUri": "/rest/storage-systems/TXQ1010307",
                "volumeUri": "/rest/storage-volumes/89118052-A367-47B6-9F60-F26073D1D85E"
            }
        ]
    },
}


@pytest.mark.resource(TestStorageVolumeAttachmentModule='storage_volume_attachments')
class TestStorageVolumeAttachmentModule(OneViewBaseTest):
    def test_should_remove_extra_presentation_by_profile_name(self):
        obj = mock.Mock()
        obj.data = MOCK_SERVER_PROFILE
        self.mock_ov_client.server_profiles.get_by_name.return_value = obj
        self.resource.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.safe_load(YAML_EXTRA_REMOVED_BY_NAME)

        StorageVolumeAttachmentModule().run()

        self.mock_ov_client.server_profiles.get_by_name.assert_called_once_with(SERVER_PROFILE_NAME)
        self.resource.remove_extra_presentations.assert_called_once_with(REPAIR_DATA)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageVolumeAttachmentModule.PRESENTATIONS_REMOVED,
            ansible_facts=dict(server_profile=MOCK_SERVER_PROFILE)
        )

    def test_should_fail_when_profile_name_not_found(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.resource.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.safe_load(YAML_EXTRA_REMOVED_BY_NAME)

        StorageVolumeAttachmentModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=StorageVolumeAttachmentModule.PROFILE_NOT_FOUND)

    def test_should_remove_extra_presentation_by_profile_uri(self):
        self.resource.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.safe_load(YAML_EXTRA_REMOVED_BY_URI)

        StorageVolumeAttachmentModule().run()

        self.resource.remove_extra_presentations.assert_called_once_with(REPAIR_DATA)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageVolumeAttachmentModule.PRESENTATIONS_REMOVED,
            ansible_facts=dict(server_profile=MOCK_SERVER_PROFILE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
