## oneview_appliance_device_snmp_v3_users
Retrieve the facts about one or more of the OneView Appliance Device SNMP v3  user resources.

#### Synopsis
  Provides an interface to manage Appliance Device SNMP v3  user resources. Can create, update, and delete.

#### Requirements (on the host that executes the module)
  * hpeOneView >=6.0.0  
  
#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Appliance Device SNMP v3  user properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Appliance Device SNMP v3  user resources. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_device_snmp_v3_users
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_device_snmp_v3_users   | Has the facts about the managed Appliance Device SNMP v3  user. |  On state 'present'. Can be null. |  dict |
