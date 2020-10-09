## oneview_storage_pool
Manage OneView Storage Pool resources.

#### Synopsis
 Provides an interface to manage Storage Pool resources. Can add and remove.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.8.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Storage Pool properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage Pool resource. `present` will ensure data properties are compliant with OneView. From API500 onwards it is only possible to update its state. `absent` will remove the resource from OneView, if it exists. From API500 onwards absent state is immutable.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_pool
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_pool   | Has the OneView facts about the Storage Pool. |  On 'present' state, but can be null. |  dict |