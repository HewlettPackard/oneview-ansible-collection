## oneview_user_facts
Retrieve the facts about one or more of the OneView Users.

#### Synopsis
 Retrieve the facts about one or more of the Users from OneView.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| userName  |   No  |  | |  User name.  |
| role  |   No  |  | |  role name.  |
| options | No  |  |  getUserRoles | Options to get role associated with username. 
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |



#### Examples

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_user_facts
```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| users   | It has all the OneView facts about the Users. |  Always, but can be null. |  dict |
| user_roles | It has all the role's associated with Users. | Always. | list |
| role   | It has all the Users with specified role. | Always. but can be null. | list |
