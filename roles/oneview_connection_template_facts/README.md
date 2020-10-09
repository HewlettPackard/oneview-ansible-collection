## oneview_connection_template_facts
Retrieve facts about the OneView Connection Templates.

#### Synopsis
 Retrieve facts about the OneView Connection Templates.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Connection Template name.  |
| options  |   No  |  | |  List with options to gather additional facts about Connection Template related resources. Options allowed: `defaultConnectionTemplate`.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_scope_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| connection_templates   | Has all the OneView facts about the Connection Templates. |  Always, except when defaultConnectionTemplate is requested. Can be null. |  dict |
| default_connection_template   | Has the facts about the Default Connection Template. |  When requested, but can be null. |  dict |
