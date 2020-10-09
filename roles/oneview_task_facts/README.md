## oneview_task_facts
Retrieve facts about the OneView Tasks.

#### Synopsis
 Retrieve facts about the OneView Tasks.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| params  |   No  |  | |  List with parameters to help filter the tasks. Params allowed: `count`, `fields`, `filter`, `query`, `sort`, `start`, and `view`.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_task_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| tasks   | The list of tasks. |  Always, but can be null. |  list |
