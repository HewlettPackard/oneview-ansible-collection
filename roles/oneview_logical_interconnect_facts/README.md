## oneview_logical_interconnect_facts
Retrieve facts about one or more of the OneView Logical Interconnects.

#### Synopsis
 Retrieve facts about one or more of the OneView Logical Interconnects.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.8.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Interconnect name.  |
| options  |   No  |  | |  List with options to gather additional facts about Logical Interconnect. Options allowed: `qos_aggregated_configuration` gets the QoS aggregated configuration for the logical interconnect. `snmp_configuration` gets the SNMP configuration for a logical interconnect. `port_monitor` gets the port monitor configuration of a logical interconnect. `internal_vlans` gets the internal VLAN IDs for the provisioned networks on a logical interconnect. `forwarding_information_base` gets the forwarding information base data for a logical interconnect. `firmware` get the installed firmware for a logical interconnect. `unassigned_ports` gets a collection of ports from the member interconnects which are eligible for assignment to an analyzer port. `unassigned_uplink_ports` gets a collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port. `telemetry_configuration` gets the telemetry configuration of the logical interconnect. `ethernet_settings` gets the Ethernet interconnect settings for the Logical Interconnect. - These options are valid just when a `name` is provided. Otherwise it will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_interconnect_type_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| ethernet_settings   | The Ethernet Interconnect Settings. |  When requested, but can be null. |  dict |
| firmware   | The installed firmware for a logical interconnect. |  When requested, but can be null. |  dict |
| forwarding_information_base   | The forwarding information base data for a logical interconnect. |  When requested, but can be null. |  dict |
| internal_vlans   | The internal VLAN IDs for the provisioned networks on a logical interconnect. |  When requested, but can be null. |  dict |
| logical_interconnects   | The list of logical interconnects. |  Always, but can be null. |  list |
| port_monitor   | The port monitor configuration of a logical interconnect. |  When requested, but can be null. |  dict |
| qos_aggregated_configuration   | The QoS aggregated configuration for the logical interconnect. |  When requested, but can be null. |  dict |
| snmp_configuration   | The SNMP configuration for a logical interconnect. |  When requested, but can be null. |  dict |
| telemetry_configuration   | The telemetry configuration of the logical interconnect. |  When requested, but can be null. |  dict |
| unassigned_ports   | A collection of ports from the member interconnects which are eligible for assignment to an analyzer port on a logical interconnect. |  When requested, but can be null. |  dict |
| unassigned_uplink_ports   | A collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port on a logical interconnect. |  When requested, but can be null. |  dict |
