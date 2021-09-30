# Ansible Collections for HPE OneView Change Log

## v6.4.0(unreleased)
This release extends the planned support of the collections to OneView REST API version 3400 (OneView v6.4).

#### Bug fixes & Enhancements
- [#141] (https://github.com/HewlettPackard/oneview-ansible-collection/issues/141) add storage to list of tags in galaxy.yml

### Modules supported in this release
- oneview_repositories
- oneview_repositories_facts

## v6.3.0
This release extends the planned support of the collections to OneView REST API version 3200 (OneView v6.3).

#### Bug fixes & Enhancements
- [#131] (https://github.com/HewlettPackard/oneview-ansible-collection/issues/131) Gather facts about a ID Pools IPV4 Subnet by name doesnt supported.

### Modules supported in this release
- oneview_appliance_configuration_timeconfig_facts
- oneview_appliance_device_snmp_v1_trap_destination
- oneview_appliance_device_snmp_v1_trap_destination_facts
- oneview_appliance_device_snmp_v3_trap_destination
- oneview_appliance_device_snmp_v3_trap_destination_facts
- oneview_appliance_device_snmp_v3_users
- oneview_appliance_device_snmp_v3_users_facts
- oneview_appliance_network_interfaces
- oneview_appliance_network_interface_facts
- oneview_appliance_proxy_configuration
- oneview_appliance_proxy_configuration_facts
- oneview_appliance_ssh_access
- oneview_appliance_ssh_access_facts
- oneview_appliance_time_and_locale_configuration
- oneview_appliance_time_and_locale_configuration_facts
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_firmware_bundle
- oneview_firmware_driver
- oneview_firmware_driver_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_id_pools
- oneview_id_pools_facts
- oneview_id_pools_ipv4_range
- oneview_id_pools_ipv4_range_facts
- oneview_id_pools_ipv4_subnet
- oneview_id_pools_ipv4_subnet_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_label
- oneview_label_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts
- oneview_user
- oneview_user_facts
- oneview_version_facts

## v6.2.0
This release extends the planned support of the collections to OneView REST API version 3000 (OneView v6.2).

#### Major changes
 1. Added support for 1 new endpoint in Server Profile Template.
   - PATCH /rest/server-profile-templates/{id}

### Modules supported in this release
- oneview_appliance_configuration_timeconfig_facts
- oneview_appliance_device_snmp_v1_trap_destination
- oneview_appliance_device_snmp_v1_trap_destination_facts
- oneview_appliance_device_snmp_v3_trap_destination
- oneview_appliance_device_snmp_v3_trap_destination_facts
- oneview_appliance_device_snmp_v3_users
- oneview_appliance_device_snmp_v3_users_facts
- oneview_appliance_ssh_access
- oneview_appliance_ssh_access_facts
- oneview_appliance_time_and_locale_configuration
- oneview_appliance_time_and_locale_configuration_facts
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_firmware_driver
- oneview_firmware_driver_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_id_pools
- oneview_id_pools_facts
- oneview_id_pools_ipv4_range
- oneview_id_pools_ipv4_range_facts
- oneview_id_pools_ipv4_subnet
- oneview_id_pools_ipv4_subnet_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_label
- oneview_label_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts
- oneview_user
- oneview_user_facts
- oneview_version_facts

## v6.1.0
This release extends the planned support of the collections to OneView REST API version 2800 (OneView v6.1) and ImageStreamer REST API version 2020 (I3S v6.1) 

#### Major changes
 1. Added support for 3 new endpoints in oneview_tasks and oneview_task_facts resource.
   - PATCH /rest/tasks/{id}
   - GET{Tree} /rest/tasks/{id}
   - GET{AggregatedTree} /rest/tasks/{id}
 2. Added support for user resource.

#### Bug fixes & Enhancements
- [#85] (https://github.com/HewlettPackard/oneview-ansible-collection/issues/85) Enhancement Request: SPP "name" too restrictive
- [#97] (https://github.com/HewlettPackard/oneview-ansible-collection/issues/97) contents.api_version

### Modules supported in this release
- image_streamer_artifact_bundle
- image_streamer_artifact_bundle_facts
- image_streamer_build_plan
- image_streamer_build_plan_facts
- image_streamer_deployment_group_facts
- image_streamer_deployment_plan
- image_streamer_deployment_plan_facts
- image_streamer_golden_image
- image_streamer_golden_image_facts
- image_streamer_os_volume_facts
- image_streamer_plan_script
- image_streamer_plan_script_facts
- oneview_appliance_configuration_timeconfig_facts
- oneview_appliance_device_snmp_v1_trap_destination
- oneview_appliance_device_snmp_v1_trap_destination_facts
- oneview_appliance_device_snmp_v3_trap_destination
- oneview_appliance_device_snmp_v3_trap_destination_facts
- oneview_appliance_device_snmp_v3_users
- oneview_appliance_device_snmp_v3_users_facts
- oneview_appliance_ssh_access
- oneview_appliance_ssh_access_facts
- oneview_appliance_time_and_locale_configuration
- oneview_appliance_time_and_locale_configuration_facts
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_firmware_driver
- oneview_firmware_driver_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_id_pools
- oneview_id_pools_facts
- oneview_id_pools_ipv4_range
- oneview_id_pools_ipv4_range_facts
- oneview_id_pools_ipv4_subnet
- oneview_id_pools_ipv4_subnet_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_label
- oneview_label_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts
- oneview_user
- oneview_user_facts
- oneview_version_facts

## v6.0.0
This release extends the planned support of the collections to OneView REST API version 2600 (OneView v6.0) and ImageStreamer REST API version 2010 (I3S v6.0) 

#### Bug fixes & Enhancements
- [#66] (https://github.com/HewlettPackard/oneview-ansible-collection/issues/66) module_utils _merge_connections_boot fails with TypeError

### Modules supported in this release
- image_streamer_artifact_bundle
- image_streamer_artifact_bundle_facts
- image_streamer_build_plan
- image_streamer_build_plan_facts
- image_streamer_deployment_group_facts
- image_streamer_deployment_plan
- image_streamer_deployment_plan_facts
- image_streamer_golden_image
- image_streamer_golden_image_facts
- image_streamer_os_volume_facts
- image_streamer_plan_script
- image_streamer_plan_script_facts
- oneview_appliance_configuration_timeconfig_facts
- oneview_appliance_device_snmp_v1_trap_destination
- oneview_appliance_device_snmp_v1_trap_destination_facts
- oneview_appliance_device_snmp_v3_trap_destination
- oneview_appliance_device_snmp_v3_trap_destination_facts
- oneview_appliance_device_snmp_v3_users
- oneview_appliance_device_snmp_v3_users_facts
- oneview_appliance_ssh_access
- oneview_appliance_ssh_access_facts
- oneview_appliance_time_and_locale_configuration
- oneview_appliance_time_and_locale_configuration_facts
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_firmware_driver
- oneview_firmware_driver_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_id_pools_ipv4_range
- oneview_id_pools_ipv4_range_facts
- oneview_id_pools_ipv4_subnet
- oneview_id_pools_ipv4_subnet_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts
- oneview_os_deployment_server
- oneview_os_deployment_server_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts

## v1.2.1
This release extends the planned support of the collections to OneView REST API version 2400 (OneView v5.6)

#### Major changes
1. Achieved idempotency for below resources.
   - Logical Interconnect Group
   - Scope
   - Server Profile
   - Server Profile Template
 
2. Added support for 4 new endpoints in oneview_logical_interconnect and oneview_logical_interconnect_facts resource.
   - POST /rest/logical-interconnects/bulk-inconsistency-validation
   - GET /rest/logical-interconnects/{id}/igmpSettings
   - PUT /rest/logical-interconnects/{id}/igmpSettings
   - PUT /rest/logical-interconnects/{id}/portFlapSettings

### Modules supported in this release
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts
- oneview_os_deployment_server
- oneview_os_deployment_server_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts

## v1.1.0
This release extends the planned support of the collections to OneView REST API version 2200 (OneView v5.5)

### Modules supported in this release
- oneview_certificates_server
- oneview_certificates_server_facts
- oneview_connection_template
- oneview_connection_template_facts
- oneview_enclosure
- oneview_enclosure_facts
- oneview_enclosure_group
- oneview_enclosure_group_facts
- oneview_ethernet_network
- oneview_ethernet_network_facts
- oneview_fc_network
- oneview_fc_network_facts
- oneview_fcoe_network
- oneview_fcoe_network_facts
- oneview_hypervisor_cluster_profile
- oneview_hypervisor_cluster_profile_facts
- oneview_hypervisor_manager
- oneview_hypervisor_manager_facts
- oneview_interconnect
- oneview_interconnect_facts
- oneview_interconnect_type_facts
- oneview_logical_enclosures
- oneview_logical_enclosures_facts
- oneview_logical_interconnect
- oneview_logical_interconnect_facts
- oneview_logical_interconnect_group
- oneview_logical_interconnect_group_facts
- oneview_network_set
- oneview_network_set_facts
- oneview_os_deployment_plan_facts
- oneview_os_deployment_server
- oneview_os_deployment_server_facts
- oneview_scope
- oneview_scope_facts
- oneview_server_hardware
- oneview_server_hardware_facts
- oneview_server_hardware_type
- oneview_server_hardware_type_facts
- oneview_server_profile
- oneview_server_profile_facts
- oneview_server_profile_template
- oneview_server_profile_template_facts
- oneview_storage_pool
- oneview_storage_pool_facts
- oneview_storage_system
- oneview_storage_system_facts
- oneview_storage_volume
- oneview_storage_volume_facts
- oneview_storage_volume_attachment
- oneview_storage_volume_attachment_facts
- oneview_storage_volume_template
- oneview_storage_volume_template_facts
- oneview_task_facts
- oneview_uplink_set
- oneview_uplink_set_facts
