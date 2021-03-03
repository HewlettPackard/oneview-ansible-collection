## oneview_appliance_device_snmp_v1_trap_destinations
Manage the Appliance Device SNMPv1 Trap Destinations.

#### Synopsis
 Provides an interface to manage the Appliance Device SNMPv1 Trap Destinations.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   No  |  | |  List with the SNMPv1 Trap Destination properties  |
| name  |   Yes  |  | |  SNMPv1 Trap Destination address  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Appliance Device SNMPv1 Trap Destinations. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_device_snmp_v1_trap_destination
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_device_snmp_v1_trap_destinations   | Has all the OneView facts about the OneView appliance SNMPv1 trap forwarding destinations. |  On state 'present'. |  dict |
