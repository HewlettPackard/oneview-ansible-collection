## oneview_sas_logical_interconnect
Manage OneView SAS Logical Interconnect resources.

#### Synopsis
Provides an interface to manage SAS Logical Interconnect resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.6.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the options.  |
| state  |   |  | <ul> <li>compliance</li>  <li>apply_configuration</li>  <li>update_firmware</li>  <li>replace_drive_enclosure</li>  </ul> |  Indicates the desired state for the SAS Logical Interconnect resource. `compliance` brings the logical interconnect back to a consistent state. `apply_configuration` Asynchronously applies or re-applies the SAS logical interconnect configuration. `update_firmware` Installs firmware to the member interconnects of a logical interconnect. `replace_drive_enclosure` Initiate the replacement operation that enables the new drive enclosure to take over as a replacement for the prior drive enclosure.
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_sas_logical_interconnect
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_interconnect   | Has the OneView facts about the SAS Logical Interconnect. |  On 'compliance', 'apply_configuration', 'replace_drive_enclosure' states, but can be null. |  dict |
| update_firmware   |Has the OneView facts about the SAS Logical interconnect firmware. |  On 'update_firmware' state, but can be null. |  dict |
