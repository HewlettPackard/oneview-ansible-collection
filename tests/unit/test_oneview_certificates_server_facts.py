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

import pytest

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import CertificatesServerFactsModule

PRESENT_CERTIFICATES = {
    "aliasName": "172.18.13.11",
    "uri": "/rest/certificates/servers/172.18.13.11",
    "data": {
        "aliasName": "172.18.13.11"
    }
}

PARAMS_GET_REMOTE = dict(
    config='config.json',
    remote="172.18.13.11",
)

PARAMS_GET_BY_ALIASNAME = dict(
    config='config.json',
    aliasName="172.18.13.11",
)

DICT_DEFAULT_CERTIFICATE = PRESENT_CERTIFICATES["data"]


@pytest.mark.resource(TestCertificatesServerFactsModule='certificates_server')
class TestCertificatesServerFactsModule(OneViewBaseTest):
    def test_should_get_remote_certificate(self):
        self.resource.data = DICT_DEFAULT_CERTIFICATE
        self.resource.get_remote.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_REMOTE

        CertificatesServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(remote_certificate=DICT_DEFAULT_CERTIFICATE)
        )

    def test_should_get_certificate_server_by_aliasname(self):
        self.resource.data = DICT_DEFAULT_CERTIFICATE
        self.resource.get_by_alias_name.return_value = self.resource
        self.mock_ansible_module.params = PARAMS_GET_BY_ALIASNAME

        CertificatesServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(certificates_server=DICT_DEFAULT_CERTIFICATE)
        )


if __name__ == '__main__':
    pytest.main([__file__])
