## oneview_san_manager_facts
Retrieve the facts about one or more of the OneView San Managers

#### Synopsis
 Retrieve the facts about one or more of the San Manager from OneView.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   |  | |  San Manager name.  |
| state  |  Yes |  | <ul> <li>present</li>  <li>add_signature</li> </ul> |  Indicates the desired state for the San Manager. `present` will ensure data properties are compliant with OneView.|


## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_san_manager_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| san_managers   | Has all the OneView facts about the San Manager. |  Always, but can be null. |  dict |
