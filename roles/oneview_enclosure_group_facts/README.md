## oneview_enclosure_group_facts
Retrieve facts about one or more of the OneView Enclosure Groups.

#### Synopsis
Retrieve facts about one or more of the Enclosure Groups from OneView.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Enclosure Group name.  |
| options  |   No  |  | |  List with options to gather additional facts about Enclosure Group. Options allowed: `configuration_script` Gets the configuration script for an Enclosure Group.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_enclosure_group_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| enclosure_group_script   | The configuration script for an Enclosure Group. |  When requested, but can be null. |  string |
| enclosure_groups   | Has all the OneView facts about the Enclosure Groups. |  Always, but can be null. |  dict |
