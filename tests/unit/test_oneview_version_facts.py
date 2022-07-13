#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import VersionFactsModule

PARAMS_GET = dict(
    config='config.json'
)

DICT_DEFAULT_VERSION = [{
    "currentVersion": 500,
    "minimumVersion": 120
}]


@pytest.mark.resource(TestVersionFactsModule='versions')
class TestVersionFactsModule(OneViewBaseTest):
    def test_should_get_appliance_current_version_and_minimum_version(self):
        self.resource.get_version.return_value = DICT_DEFAULT_VERSION
        self.mock_ansible_module.params = PARAMS_GET
        VersionFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(version=DICT_DEFAULT_VERSION)
        )


if __name__ == '__main__':
    pytest.main([__file__])
