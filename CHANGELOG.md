# Ansible Collections for HPE OneView Change Log

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
