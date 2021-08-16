#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2021) Hewlett Packard Enterprise Development LP
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
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ApplianceProxyConfigurationModule

ERROR_MSG = 'Fake message error'

DEFAULT_PARAMS = dict(
    server="1.1.1.1",
    port=443,
    username="testuser",
    password="test",
    communicationProtocol="HTTP"
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=DEFAULT_PARAMS,
)


PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=DEFAULT_PARAMS)


@pytest.mark.resource(TestApplianceProxyConfigurationModule='appliance_proxy_configuration')
class TestApplianceProxyConfigurationModule(OneViewBaseTest):
    def test_should_create_proxy_configuration(self):
        self.resource.get_by_proxy.return_value = None
        self.resource.data = DEFAULT_PARAMS
        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceProxyConfigurationModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceProxyConfigurationModule.MSG_CREATED,
            ansible_facts=dict(appliance_proxy_configuration=DEFAULT_PARAMS)
        )

    def test_should_do_nothing_when_proxy_configuration_exists(self):
        self.resource.data = DEFAULT_PARAMS
        self.resource.get_by_proxy.return_value = self.resource

        self.resource.create.return_value = self.resource

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        ApplianceProxyConfigurationModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceProxyConfigurationModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(appliance_proxy_configuration=DEFAULT_PARAMS)
        )

    def test_should_remove_proxy_configuration(self):
        self.resource.get_by_proxy.return_value = [DEFAULT_PARAMS]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceProxyConfigurationModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ApplianceProxyConfigurationModule.MSG_DELETED
        )

    def test_should_do_nothing_when_proxy_configuration_not_exist(self):
        self.resource.get_by_proxy.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        ApplianceProxyConfigurationModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ApplianceProxyConfigurationModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    pytest.main([__file__])
