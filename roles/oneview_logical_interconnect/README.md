## oneview_logical_interconnect
Manage OneView Logical Interconnect resources.

#### Synopsis
Provides an interface to manage Logical Interconnect resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.6.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the options.  |
| state  |   |  | <ul> <li>compliant</li>  <li>ethernet_settings_updated</li>  <li>internal_networks_updated</li>  <li>settings_updated</li>  <li>forwarding_information_base_generated</li>  <li>qos_aggregated_configuration_updated</li>  <li>snmp_configuration_updated</li>  <li>port_monitor_updated</li>  <li>configuration_updated</li>  <li>firmware_installed</li>  <li>telemetry_configuration_updated</li>   </ul> |  Indicates the desired state for the Logical Interconnect resource. `compliant` brings the logical interconnect back to a consistent state. `ethernet_settings_updated` updates the Ethernet interconnect settings for the logical interconnect. `internal_networks_updated` updates the internal networks on the logical interconnect. This operation is non-idempotent. `settings_updated` updates the Logical Interconnect settings. `forwarding_information_base_generated` generates the forwarding information base dump file for the logical interconnect. This operation is non-idempotent and asynchronous. `qos_aggregated_configuration_updated` updates the QoS aggregated configuration for the logical interconnect. `snmp_configuration_updated` updates the SNMP configuration for the logical interconnect. `port_monitor_updated` updates the port monitor configuration of a logical interconnect. `configuration_updated` asynchronously applies or re-applies the logical interconnect configuration to all managed interconnects. This operation is non-idempotent. `firmware_installed` installs firmware to a logical interconnect. The three operations that are supported for the firmware update are Stage (uploads firmware to the interconnect), Activate (installs firmware on the interconnect) and Update (which does a Stage and Activate in a sequential manner). All of them are non-idempotent. `telemetry_configuration_updated` updates the telemetry configuration of a logical interconnect. `scopes_updated` updates the scopes associated with the logical interconnect.
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_logical_interconnect
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_fib   | Has the OneView facts about the Forwarding information Base. |  On 'forwarding_information_base_generated' state, but can be null. |  dict |
| li_firmware   | Has the OneView facts about the installed Firmware. |  On 'firmware_installed' state, but can be null. |  dict |
| port_monitor   | Has the OneView facts about the Port Monitor Configuration. |  On 'port_monitor_updated' state, but can be null. |  dict |
| qos_configuration   | Has the OneView facts about the QoS Configuration. |  On 'qos_aggregated_configuration_updated' state, but can be null. |  dict |
| scope_uris   | Has the scope URIs the specified logical interconnect is inserted into. |  On 'scopes_updated' state, but can be null. |  dict |
| snmp_configuration   | Has the OneView facts about the SNMP Configuration. |  On 'snmp_configuration_updated' state, but can be null. |  dict |
| igmp_settings   | Has the OneView facts about the IGMP settings. |  On 'igmp_settings_updated' state, but can be null. |  dict |
| port_flap_settings   | Has the OneView facts about the port flap settings. |  On 'port_flap_settings_updated' state, but can be null. |  dict |
| li_inconsistency_report   | Has the OneView facts about the bulk inconsistency report. |  On 'bulk_inconsistency_validated' state, but can be null. |  dict |
| storage_volume_template   | Has the OneView facts about the Logical Interconnect. |  On 'compliant', 'ethernet_settings_updated', 'internal_networks_updated', 'settings_updated',               and 'configuration_updated' states, but can be null. |  dict |
| telemetry_configuration   | Has the OneView facts about the Telemetry Configuration. |  On 'telemetry_configuration_updated' state, but can be null. |  dict |
