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

"""
This module was created because the code in this repository is shared with Ansible Core.
So, to avoid merging issues, and maintaining the tests code equal, we create a unique file to
configure the imports that change from one repository to another.
"""

import sys
from plugins.module_utils import icsp, oneview

ONEVIEW_MODULE_UTILS_PATH = 'plugins.module_utils.oneview'

sys.modules['ansible.module_utils.oneview'] = oneview
sys.modules['ansible.module_utils.icsp'] = icsp

from plugins.module_utils.oneview import (OneViewModuleBase,
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
from plugins.modules.icsp import ICspHelper
from plugins.modules.image_streamer_artifact_bundle import ArtifactBundleModule
from plugins.modules.image_streamer_artifact_bundle_facts import ArtifactBundleFactsModule
from plugins.modules.image_streamer_build_plan import BuildPlanModule
from plugins.modules.image_streamer_build_plan_facts import BuildPlanFactsModule
from plugins.modules.image_streamer_deployment_group_facts import DeploymentGroupFactsModule
from plugins.modules.image_streamer_deployment_plan import DeploymentPlanModule
from plugins.modules.image_streamer_deployment_plan_facts import DeploymentPlanFactsModule
from plugins.modules.image_streamer_golden_image import GoldenImageModule
from plugins.modules.image_streamer_golden_image_facts import GoldenImageFactsModule
from plugins.modules.image_streamer_os_volume_facts import OsVolumeFactsModule
from plugins.modules.mage_streamer_plan_script import PlanScriptModule
from plugins.modules.image_streamer_plan_script_facts import PlanScriptFactsModule
from plugins.modules.oneview_alert_facts import AlertFactsModule
from plugins.modules.oneview_appliance_device_read_community import ApplianceDeviceReadCommunityModule
from plugins.modules.oneview_appliance_device_read_community_facts import ApplianceDeviceReadCommunityFactsModule
from plugins.modules.oneview_appliance_device_snmp_v1_trap_destination import ApplianceDeviceSnmpV1TrapDestinationsModule
from plugins.modules.oneview_appliance_device_snmp_v1_trap_destination_facts import ApplianceDeviceSnmpV1TrapDestinationsFactsModule
from plugins.modules.oneview_appliance_device_snmp_v3_trap_destination import ApplianceDeviceSnmpV3TrapDestinationsModule
from plugins.modules.oneview_appliance_device_snmp_v3_trap_destination_facts import ApplianceDeviceSnmpV3TrapDestinationsFactsModule
from plugins.modules.oneview_appliance_device_snmp_v3_users import ApplianceDeviceSnmpV3UsersModule
from plugins.modules.oneview_appliance_device_snmp_v3_users_facts import ApplianceDeviceSnmpV3UsersFactsModule
from plugins.modules.oneview_appliance_configuration_timeconfig_facts import ApplianceConfigurationTimeconfigFactsModule
from plugins.modules.oneview_appliance_ssh_access_facts import ApplianceSshAccessFactsModule
from plugins.modules.oneview_appliance_ssh_access import ApplianceSshAccessModule
from plugins.modules.oneview_appliance_time_and_locale_configuration_facts import ApplianceTimeAndLocaleConfigurationFactsModule
from plugins.modules.oneview_appliance_time_and_locale_configuration import ApplianceTimeAndLocaleConfigurationModule
from plugins.modules.oneview_certificates_server import CertificatesServerModule
from plugins.modules.oneview_certificates_server_facts import CertificatesServerFactsModule
from plugins.modules.oneview_connection_template import ConnectionTemplateModule
from plugins.modules.oneview_connection_template_facts import ConnectionTemplateFactsModule
from plugins.modules.oneview_datacenter import DatacenterModule
from plugins.modules.oneview_datacenter_facts import DatacenterFactsModule
from plugins.modules.oneview_drive_enclosure import DriveEnclosureModule
from plugins.modules.oneview_drive_enclosure_facts import DriveEnclosureFactsModule
from plugins.modules.oneview_enclosure import EnclosureModule
from plugins.modules.oneview_enclosure_facts import EnclosureFactsModule
from plugins.modules.oneview_enclosure_group import EnclosureGroupModule
from plugins.modules.oneview_enclosure_group_facts import EnclosureGroupFactsModule
from plugins.modules.oneview_ethernet_network import EthernetNetworkModule
from plugins.modules.oneview_ethernet_network_facts import EthernetNetworkFactsModule
from plugins.modules.oneview_event import EventModule
from plugins.modules.oneview_event_facts import EventFactsModule
from plugins.modules.oneview_fabric import FabricModule
from plugins.modules.oneview_fabric_facts import FabricFactsModule
from plugins.modules.oneview_fc_network import FcNetworkModule
from plugins.modules.oneview_fc_network_facts import FcNetworkFactsModule
from plugins.modules.oneview_fcoe_network import FcoeNetworkModule
from plugins.modules.oneview_fcoe_network_facts import FcoeNetworkFactsModule
from plugins.modules.oneview_firmware_bundle import FirmwareBundleModule
from plugins.modules.oneview_firmware_driver import FirmwareDriverModule
from plugins.modules.oneview_firmware_driver_facts import FirmwareDriverFactsModule
from plugins.modules.oneview_hypervisor_cluster_profile import HypervisorClusterProfileModule
from plugins.modules.oneview_hypervisor_cluster_profile_facts import HypervisorClusterProfileFactsModule
from plugins.modules.oneview_hypervisor_manager import HypervisorManagerModule
from plugins.modules.oneview_hypervisor_manager_facts import HypervisorManagerFactsModule
from plugins.modules.oneview_id_pools_ipv4_subnet import IdPoolsIpv4SubnetModule
from plugins.modules.oneview_id_pools_ipv4_subnet_facts import IdPoolsIpv4SubnetFactsModule
from plugins.modules.oneview_id_pools_ipv4_range import IdPoolsIpv4RangeModule
from plugins.modules.oneview_id_pools_ipv4_range_facts import IdPoolsIpv4RangeFactsModule
from plugins.modules.oneview_interconnect import InterconnectModule
from plugins.modules.oneview_interconnect_facts import InterconnectFactsModule
from plugins.modules.oneview_interconnect_link_topology_facts import InterconnectLinkTopologyFactsModule
from plugins.modules.oneview_interconnect_type_facts import InterconnectTypeFactsModule
from plugins.modules.oneview_internal_link_set_facts import InternalLinkSetFactsModule
from plugins.modules.oneview_logical_downlinks_facts import LogicalDownlinksFactsModule
from plugins.modules.oneview_logical_enclosure import LogicalEnclosureModule
from plugins.modules.oneview_logical_enclosure_facts import LogicalEnclosureFactsModule
from plugins.modules.oneview_logical_interconnect import LogicalInterconnectModule
from plugins.modules.oneview_logical_interconnect_facts import LogicalInterconnectFactsModule
from plugins.modules.oneview_logical_interconnect_group import LogicalInterconnectGroupModule
from plugins.modules.oneview_logical_interconnect_group_facts import LogicalInterconnectGroupFactsModule
from plugins.modules.oneview_logical_switch import LogicalSwitchModule
from plugins.modules.oneview_logical_switch_facts import LogicalSwitchFactsModule
from plugins.modules.oneview_logical_switch_group import LogicalSwitchGroupModule
from plugins.modules.oneview_logical_switch_group_facts import LogicalSwitchGroupFactsModule
from plugins.modules.oneview_login_detail_facts import LoginDetailFactsModule
from plugins.modules.oneview_managed_san import ManagedSanModule
from plugins.modules.oneview_managed_san_facts import ManagedSanFactsModule
from plugins.modules.plugins.modules.oneview_network_set import NetworkSetModule
from plugins.modules.plugins.modules.oneview_network_set_facts import NetworkSetFactsModule
from plugins.modules.oneview_os_deployment_plan_facts import OsDeploymentPlanFactsModule
from plugins.modules.oneview_os_deployment_server import OsDeploymentServerModule
from plugins.modules.oneview_os_deployment_server_facts import OsDeploymentServerFactsModule
from plugins.modules.oneview_power_device import PowerDeviceModule
from plugins.modules.oneview_power_device_facts import PowerDeviceFactsModule
from plugins.modules.oneview_rack import RackModule
from plugins.modules.oneview_rack_facts import RackFactsModule
from plugins.modules.oneview_san_manager import SanManagerModule
from plugins.modules.oneview_san_manager_facts import SanManagerFactsModule
from plugins.modules.oneview_sas_interconnect import SasInterconnectModule
from plugins.modules.oneview_sas_interconnect_facts import SasInterconnectFactsModule
from plugins.modules.oneview_sas_interconnect_type_facts import SasInterconnectTypeFactsModule
from plugins.modules.oneview_sas_logical_interconnect import SasLogicalInterconnectModule
from plugins.modules.oneview_sas_logical_interconnect_facts import SasLogicalInterconnectFactsModule
from plugins.modules.oneview_sas_logical_interconnect_group import SasLogicalInterconnectGroupModule
from plugins.modules.oneview_sas_logical_interconnect_group_facts import SasLogicalInterconnectGroupFactsModule
from plugins.modules.oneview_sas_logical_jbod_attachment_facts import SasLogicalJbodAttachmentFactsModule
from plugins.modules.oneview_sas_logical_jbod_facts import SasLogicalJbodFactsModule
from plugins.modules.oneview_scope import ScopeModule
from plugins.modules.oneview_scope_facts import ScopeFactsModule
from plugins.modules.oneview_server_hardware import ServerHardwareModule
from plugins.modules.oneview_server_hardware_facts import ServerHardwareFactsModule
from plugins.modules.oneview_server_hardware_type import ServerHardwareTypeModule
from plugins.modules.oneview_server_hardware_type_facts import ServerHardwareTypeFactsModule
from plugins.modules.oneview_server_profile import ServerProfileModule
from plugins.modules.oneview_server_profile_facts import ServerProfileFactsModule
from plugins.modules.oneview_server_profile_template import ServerProfileTemplateModule
from plugins.modules.oneview_server_profile_template_facts import ServerProfileTemplateFactsModule
from plugins.modules.oneview_storage_pool import StoragePoolModule
from plugins.modules.oneview_storage_pool_facts import StoragePoolFactsModule
from plugins.modules.oneview_storage_system import StorageSystemModule
from plugins.modules.oneview_storage_system_facts import StorageSystemFactsModule
from plugins.modules.oneview_storage_volume_attachment import StorageVolumeAttachmentModule
from plugins.modules.oneview_storage_volume_attachment_facts import StorageVolumeAttachmentFactsModule
from plugins.modules.oneview_storage_volume_template import StorageVolumeTemplateModule
from plugins.modules.oneview_storage_volume_template_facts import StorageVolumeTemplateFactsModule
from plugins.modules.oneview_switch import SwitchModule
from plugins.modules.oneview_switch_facts import SwitchFactsModule
from plugins.modules.oneview_switch_type_facts import SwitchTypeFactsModule
from plugins.modules.oneview_task_facts import TaskFactsModule
from plugins.modules.oneview_unmanaged_device import UnmanagedDeviceModule
from plugins.modules.oneview_unmanaged_device_facts import UnmanagedDeviceFactsModule
from plugins.modules.oneview_uplink_set import UplinkSetModule
from plugins.modules.oneview_uplink_set_facts import UplinkSetFactsModule
from plugins.modules.oneview_user import UserModule
from plugins.modules.oneview_user_facts import UserFactsModule
from plugins.modules.oneview_volume import VolumeModule
from plugins.modules.oneview_volume_facts import VolumeFactsModule
from plugins.modules.oneview_version_facts import VersionFactsModule
