## oneview_sas_logical_jbod_facts
Retrieve facts about one or more of the OneView SAS logical JBODs.

#### Synopsis
Retrieve facts about one or more of the SAS logical JBODs from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  SAS logical JBOD name  |
| options  |   No  |  | |  List with options to gather additional facts about SAS logical JBOD. 
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_sas_logical_jbod_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_jbod_facts   | Has all the OneView facts about the SAS Logical JBODs. |  Always, but can be null. |  dict |
