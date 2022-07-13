## oneview_appliance_device_snmp_v3_trap_destinations
Manage the Appliance Device SNMPv3 Trap Destinations.

#### Synopsis
 Provides an interface to manage the Appliance Device SNMPv3 Trap Destinations.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   Yes  |  | |  SNMPv3 Trap Destination Address  |
| data  |   No  |  | |  List with the SNMPv3 Trap Destinations properties  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Appliance Device SNMPv3 Trap Destinations. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_device_snmp_v3_trap_destination
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_device_snmp_v3_trap_destinations   | Has all the OneView facts about the OneView appliance SNMPv3 Trap Destination. |  On state 'present'. Can be null. |  dict |
