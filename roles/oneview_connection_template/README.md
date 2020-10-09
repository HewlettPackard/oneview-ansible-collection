## oneview_connection_template
Manage the OneView Connection Template resources.

#### Synopsis
 Provides an interface to manage the Connection Template resources. Can update.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Connection Template properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li> </ul> |  Indicates the desired state for the Connection Template resource. `present` will ensure data properties are compliant with OneView.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_connection_template
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| connection_template   | Has the OneView facts about the Connection Template. |  On 'present' state, but can be null. |  dict |
