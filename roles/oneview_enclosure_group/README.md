## oneview_enclosure_group
Manage OneView Enclosure Group resources.

#### Synopsis
Provides an interface to manage Enclosure Group resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Enclosure Group properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Enclosure Group resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_enclosure_group
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_group   | Has the facts about the Enclosure Group. |  On state 'present'. Can be null. |  dict |
