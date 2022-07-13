## oneview_appliance_device_snmp_v1_trap_destinations_facts
Retrieve the facts about the OneView appliance SNMPv1 trap forwarding destinations.

#### Synopsis
 The appliance has the ability to forward events received from monitored or managed server hardware to the specified destinations as SNMPv1 traps. This module retrives the facts about the appliance SNMPv1 trap forwarding destinations.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of trap destination.  |
| uri  |   No  |  | |  Uri of trap destination.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_device_snmp_v1_trap_destination_facts
```

## License

Apache


#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_device_snmp_v1_trap_destinations   | Has all the OneView facts about the OneView appliance SNMPv1 trap forwarding destinations. |  Always. |  dict |
