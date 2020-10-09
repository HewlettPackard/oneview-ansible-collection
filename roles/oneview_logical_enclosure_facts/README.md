## oneview_logical_enclosure_facts
Retrieve facts about one or more of the OneView Logical Enclosures.

#### Synopsis
Retrieve facts about one or more of the Logical Enclosures from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Logical Enclosure name.  |
| options  |   No  |  | |  List with options to gather additional facts about a Logical Enclosure and related resources. Options allowed: script.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_logical_enclosure_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| logical_enclosure_script   | Has the facts about the script of a Logical Enclosure. |  When required, but can be null. |  dict |
| logical_enclosures   | Has all the OneView facts about the Logical Enclosures. |  Always, but can be null. |  dict |
