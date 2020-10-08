## oneview_scope_facts
Retrieve facts about one or more of the OneView Scopes.

#### Synopsis
 Retrieve facts about one or more of the Scopes from OneView.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the scope.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: c(start): The first item to return, using 0-based indexing. c(count): The number of resources to return. c(query): A general query string to narrow the list of resources returned. c(sort): The sort order of the returned data set. c(view): Returns a specific subset of the attributes of the resource or collection, by specifying the name of a predefined view.  |


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
| scopes   | Has all the OneView facts about the Scopes. |  Always, but can be null. |  dict |
