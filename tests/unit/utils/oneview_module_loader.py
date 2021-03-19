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

"""
This module was created because the code in this repository is shared with Ansible Core.
So, to avoid merging issues, and maintaining the tests code equal, we create a unique file to
configure the imports that change from one repository to another.
"""

import sys
from ansible_collections.hpe.oneview.plugins.module_utils import icsp, oneview

ONEVIEW_MODULE_UTILS_PATH = 'ansible_collections.hpe.oneview.plugins.module_utils.oneview'

sys.modules['ansible.module_utils.oneview'] = oneview
sys.modules['ansible.module_utils.icsp'] = icsp

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import (OneViewModuleBase,
                                                                          OneViewClient,
                                                                          OneViewModuleException,
                                                                          OneViewModuleTaskError,
                                                                          OneViewModuleValueError,
                                                                          OneViewModuleResourceNotFound,
                                                                          SPKeys,
                                                                          ServerProfileMerger,
                                                                          ServerProfileReplaceNamesByUris,
                                                                          _str_sorted,
                                                                          merge_list_by_key,
                                                                          transform_list_to_dict,
                                                                          compare,
                                                                          get_logger)
# from ansible_collections.hpe.oneview.plugins.module_utils import ICspHelper
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_artifact_bundle import ArtifactBundleModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_artifact_bundle_facts import ArtifactBundleFactsModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_build_plan import BuildPlanModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_build_plan_facts import BuildPlanFactsModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_deployment_group_facts import DeploymentGroupFactsModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_deployment_plan import DeploymentPlanModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_deployment_plan_facts import DeploymentPlanFactsModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_golden_image import GoldenImageModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_golden_image_facts import GoldenImageFactsModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_os_volume_facts import OsVolumeFactsModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_plan_script import PlanScriptModule
from ansible_collections.hpe.oneview.plugins.modules.image_streamer_plan_script_facts import PlanScriptFactsModule
# from oneview_alert_facts import AlertFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_read_community import ApplianceDeviceReadCommunityModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_read_community_facts import ApplianceDeviceReadCommunityFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_snmp_v1_trap_destinations import ApplianceDeviceSnmpV1TrapDestinationsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_snmp_v1_trap_destinations_facts \
    import ApplianceDeviceSnmpV1TrapDestinationsFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_snmp_v3_trap_destinations import ApplianceDeviceSnmpV3TrapDestinationsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_snmp_v3_trap_destinations_facts \
    import ApplianceDeviceSnmpV3TrapDestinationsFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_snmp_v3_users import ApplianceDeviceSnmpV3UsersModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_device_snmp_v3_users_facts import ApplianceDeviceSnmpV3UsersFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_configuration_timeconfig_facts import ApplianceConfigurationTimeconfigFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_ssh_access_facts import ApplianceSshAccessFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_ssh_access import ApplianceSshAccessModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_time_and_locale_configuration_facts import ApplianceTimeAndLocaleConfigurationFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_appliance_time_and_locale_configuration import ApplianceTimeAndLocaleConfigurationModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_certificates_server import CertificatesServerModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_certificates_server_facts import CertificatesServerFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_connection_template import ConnectionTemplateModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_connection_template_facts import ConnectionTemplateFactsModule
# from oneview_datacenter import DatacenterModule
# from oneview_datacenter_facts import DatacenterFactsModule
# from oneview_drive_enclosure import DriveEnclosureModule
# from oneview_drive_enclosure_facts import DriveEnclosureFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_enclosure import EnclosureModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_enclosure_facts import EnclosureFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_enclosure_group import EnclosureGroupModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_enclosure_group_facts import EnclosureGroupFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_ethernet_network import EthernetNetworkModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_ethernet_network_facts import EthernetNetworkFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_event import EventModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_event_facts import EventFactsModule
# from oneview_fabric import FabricModule
# from oneview_fabric_facts import FabricFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_fc_network import FcNetworkModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_fc_network_facts import FcNetworkFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_fcoe_network import FcoeNetworkModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_fcoe_network_facts import FcoeNetworkFactsModule
# from oneview_firmware_bundle import FirmwareBundleModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_firmware_driver import FirmwareDriverModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_firmware_driver_facts import FirmwareDriverFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_hypervisor_cluster_profile import HypervisorClusterProfileModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_hypervisor_cluster_profile_facts import HypervisorClusterProfileFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_hypervisor_manager import HypervisorManagerModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_hypervisor_manager_facts import HypervisorManagerFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_id_pools_ipv4_subnet import IdPoolsIpv4SubnetModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_id_pools_ipv4_subnet_facts import IdPoolsIpv4SubnetFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_id_pools_ipv4_range import IdPoolsIpv4RangeModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_id_pools_ipv4_range_facts import IdPoolsIpv4RangeFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_interconnect import InterconnectModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_interconnect_facts import InterconnectFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_interconnect_link_topology_facts import InterconnectLinkTopologyFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_interconnect_type_facts import InterconnectTypeFactsModule
# from oneview_internal_link_set_facts import InternalLinkSetFactsModule
# from oneview_logical_downlinks_facts import LogicalDownlinksFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_logical_enclosure import LogicalEnclosureModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_logical_enclosure_facts import LogicalEnclosureFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_logical_interconnect import LogicalInterconnectModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_logical_interconnect_facts import LogicalInterconnectFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_logical_interconnect_group import LogicalInterconnectGroupModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_logical_interconnect_group_facts import LogicalInterconnectGroupFactsModule
# from oneview_logical_switch import LogicalSwitchModule
# from oneview_logical_switch_facts import LogicalSwitchFactsModule
# from oneview_logical_switch_group import LogicalSwitchGroupModule
# from oneview_logical_switch_group_facts import LogicalSwitchGroupFactsModule
# from oneview_login_detail_facts import LoginDetailFactsModule
# from oneview_managed_san import ManagedSanModule
# from oneview_managed_san_facts import ManagedSanFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_network_set import NetworkSetModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_network_set_facts import NetworkSetFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_os_deployment_plan_facts import OsDeploymentPlanFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_os_deployment_server import OsDeploymentServerModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_os_deployment_server_facts import OsDeploymentServerFactsModule
# from oneview_power_device import PowerDeviceModule
# from oneview_power_device_facts import PowerDeviceFactsModule
# from oneview_rack import RackModule
# from oneview_rack_facts import RackFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_san_manager import SanManagerModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_san_manager_facts import SanManagerFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_interconnect import SasInterconnectModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_interconnect_facts import SasInterconnectFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_interconnect_type_facts import SasInterconnectTypeFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_logical_interconnect import SasLogicalInterconnectModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_logical_interconnect_facts import SasLogicalInterconnectFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_logical_interconnect_group import SasLogicalInterconnectGroupModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_logical_interconnect_group_facts import SasLogicalInterconnectGroupFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_logical_jbod_attachment_facts import SasLogicalJbodAttachmentFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_sas_logical_jbod_facts import SasLogicalJbodFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_scope import ScopeModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_scope_facts import ScopeFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_hardware import ServerHardwareModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_hardware_facts import ServerHardwareFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_hardware_type import ServerHardwareTypeModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_hardware_type_facts import ServerHardwareTypeFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_profile import ServerProfileModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_profile_facts import ServerProfileFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_profile_template import ServerProfileTemplateModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_server_profile_template_facts import ServerProfileTemplateFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_pool import StoragePoolModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_pool_facts import StoragePoolFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_system import StorageSystemModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_system_facts import StorageSystemFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_volume_attachment import StorageVolumeAttachmentModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_volume_attachment_facts import StorageVolumeAttachmentFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_volume_template import StorageVolumeTemplateModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_storage_volume_template_facts import StorageVolumeTemplateFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_switch import SwitchModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_switch_facts import SwitchFactsModule
# from ansible_collections.hpe.oneview.plugins.modules.oneview_switch_type_facts import SwitchTypeFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_task_facts import TaskFactsModule
# from oneview_unmanaged_device import UnmanagedDeviceModule
# from oneview_unmanaged_device_facts import UnmanagedDeviceFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_uplink_set import UplinkSetModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_uplink_set_facts import UplinkSetFactsModule
# from oneview_user import UserModule
# from oneview_user_facts import UserFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_volume import VolumeModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_volume_facts import VolumeFactsModule
from ansible_collections.hpe.oneview.plugins.modules.oneview_version_facts import VersionFactsModule
