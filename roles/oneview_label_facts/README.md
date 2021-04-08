## oneview_label_facts
Retrieve facts about one or more of the OneView labels. 

#### Synopsis
 Retrieve facts about one or more of the labels from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 6.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Label name.  |
| resourceUri	| No	| | | Uri of the resource from which the labels needs to be retrieved. |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  | `name_prefix` :  Filters the labels returned by the given prefix. All labels returned will have a name that starts with the given namePrefix. `category`: Filters the labels returned to those assigned to resources with the given category. Multiple category parameters can be supplied. `fields`:  Specifies which fields should be returned in the result set.

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_label_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| label   | The named servers for a label. |  When requested, but can be null. |  dict |
