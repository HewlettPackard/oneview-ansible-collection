## oneview_fcoe_network_facts
Retrieve the facts about one or more of the OneView FCoE Networks

#### Synopsis
 Retrieve the facts about one or more of the FCoE Networks from OneView.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   |  | |  FCoE Network name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_fcoe_network_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| fcoe_networks   | Has all the OneView facts about the FCoE Networks. |  Always, but can be null. |  dict |
