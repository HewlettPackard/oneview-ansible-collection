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

import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import ImageStreamerBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ArtifactBundleFactsModule


@pytest.mark.resource(TestArtifactBundleFactsModule='artifact_bundles')
class TestArtifactBundleFactsModule(ImageStreamerBaseFactsTest):
    """
    ImageStreamerBaseFactsTest has common tests for the parameters support.
    """

    ARTIFACT_BUNDLE = dict(name="HPE-ImageStreamer-Developer-2016-09-12", uri="/rest/artifact-bundles/a2f97f20-160c-4c78-8185-1f31f86efaf7")

    def test_get_all_artifact_bundles(self):
        self.resource.get_all.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.EXAMPLES[0]['image_streamer_artifact_bundle_facts']

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE])
        )

    def test_get_an_artifact_bundle_by_name(self):
        self.resource.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.EXAMPLES[4]['image_streamer_artifact_bundle_facts']

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE])
        )

    def test_get_all_backups(self):
        self.resource.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.resource.get_all_backups.return_value = [self.ARTIFACT_BUNDLE]

        self.mock_ansible_module.params = self.EXAMPLES[6]['image_streamer_artifact_bundle_facts']

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundle_backups=[self.ARTIFACT_BUNDLE])
        )


if __name__ == '__main__':
    pytest.main([__file__])
