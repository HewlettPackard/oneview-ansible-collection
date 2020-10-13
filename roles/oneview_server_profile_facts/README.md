## oneview_server_profile_facts
Manage OneView Server Profile resources.

#### Synopsis
Provides an interface to retrieve facts about Server Profile resources.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   |  | |  Server Profile name.  |
| options  |   |  | |  List with options to gather additional facts about Server Profile related resources. Options allowed: `schema`, `compliancePreview`, `profilePorts`, `messages`, `transformation`, `available_networks`, `available_servers`, `available_storage_system`, `available_storage_systems`, `available_targets`, `newProfileTemplate`,  To gather facts about `compliancePreview`, `messages`, `newProfileTemplate` and `transformation` a Server Profile name is required. Otherwise, these options will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |
| uri  |   |  | |  Server Profile uri.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_server_profile_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_profile_facts   | Has the facts about the managed OneView Server Profile. |  On state 'present'. Can be null. |  dict |
