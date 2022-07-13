## oneview_logical_enclosure
Manage OneView Logical Enclosure resources.

#### Synopsis
Provides an interface to manage Logical Enclosure resources. Can create, update, update firmware, perform dump, update configuration script, reapply configuration, update from group, or delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Logical Enclosure properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>firmware_updated</li>  <li>script_updated</li>  <li>dumped</li>  <li>reconfigured</li>  <li>updated_from_group</li>  <li>absent</li> </ul> |  Indicates the desired state for the Logical Enclosure resource. `present` ensures data properties are compliant with OneView. You can rename the enclosure providing an attribute `newName`. `firmware_updated` updates the firmware for the Logical Enclosure. `script_updated` updates the Logical Enclosure configuration script. `dumped` generates a support dump for the Logical Enclosure. `reconfigured` reconfigures all enclosures associated with a logical enclosure. `updated_from_group` makes the logical enclosure consistent with the enclosure group. `absent` will remove the resource from OneView, if it exists.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_logical_enclosure
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| configuration_script  | Has the facts about the Logical Enclosure configuration script. |  On state 'script_updated'. Can be null. |  dict |
| generated_dump_uri    | Has the facts about the Logical Enclosure generated support dump URI. |  On state 'dumped'. Can be null. |  dict |
| logical_enclosure     | Has the facts about the OneView Logical Enclosure. |  On states 'present', 'firmware_updated', 'reconfigured', 'updated_from_group', and 'absent'. Can be null. |  dict |
