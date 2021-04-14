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

from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewBaseFactsTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import InterconnectLinkTopologyFactsModule

INTERCONNECT_LINK_TOPOLOGIES = [{"name": "Interconnect Link Topology 1"},
                                {"name": "Interconnect Link Topology 2"},
                                {"name": "Interconnect Link Topology 3"}]

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Interconnect Link Topology Name 2"
)


@pytest.mark.resource(TestInterconnectLinkTopologyFactsModule='interconnect_link_topologies')
class TestInterconnectLinkTopologyFactsModule(OneViewBaseFactsTest):
    def test_should_get_all_interconnect_link_topologies(self):
        self.resource.get_all.return_value = INTERCONNECT_LINK_TOPOLOGIES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        InterconnectLinkTopologyFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_link_topologies=(INTERCONNECT_LINK_TOPOLOGIES))
        )

    def test_should_get_all_interconnect_link_topology_by_name(self):
        self.resource.get_by.return_value = [INTERCONNECT_LINK_TOPOLOGIES[1]]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        InterconnectLinkTopologyFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_link_topologies=([INTERCONNECT_LINK_TOPOLOGIES[1]]))
        )


if __name__ == '__main__':
    pytest.main([__file__])
