## oneview_storage_system_facts
Retrieve facts about the OneView Storage Systems

#### Synopsis
 Retrieve facts about the Storage Systems from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.8.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   |  | |  Storage System name.  |
| options  |   |  | |  List with options to gather additional facts about a Storage System and related resources. Options allowed: `hostTypes` gets the list of supported host types. `storagePools` gets a list of storage pools belonging to the specified storage system. `reachablePorts` gets a list of storage system reachable ports. Accepts `params`. An additional `networks` list param can be used to restrict the search for only these ones. `templates` gets a list of storage templates belonging to the storage system.  To gather facts about `storagePools`, `reachablePorts`, and `templates` it is required to inform either the argument `name`, `ip_hostname`, or `hostname`. Otherwise, this option will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |
| storage_hostname  |   |  | |  Storage System IP or hostname.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_system_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_system_host_types   | Has all the OneView facts about the supported host types. |  When requested, but can be null. |  dict |
| storage_system_pools   | Has all the OneView facts about the Storage Systems - Storage Pools. |  When requested, but can be null. |  dict |
| storage_system_reachable_ports   | Has all the OneView facts about the Storage Systems reachable ports. |  When requested, but can be null. |  dict |
| storage_system_templates   | Has all the OneView facts about the Storage Systems - Storage Templates. |  When requested, but can be null. |  dict |
| storage_systems   | Has all the OneView facts about the Storage Systems. |  Always, but can be null. |  dict |
