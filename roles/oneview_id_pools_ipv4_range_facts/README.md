## oneview_id_pools_ipv4_range_facts
Manage OneView ID Pools IPv4 range resources.

#### Synopsis
Provides an interface to retrieve facts about ID Pools IPv4 Range Facts resources.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   |  | |  IPv4 Range name.  |
| options  | No  |  | |  List with options to gather additional facts about  ID Pools IPv4 Range related resources. Options allowed: `schema`, `freeFragments`, `allocatedFragments`. To gather facts about IPv4 Range. |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |
| uri  |   |  | |  IPv4 Range uri.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_id_pools_ipv4_range_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| id_pools_ipv4_ranges   | Has the facts about the managed OneView ID Pools IPv4 Range |  On state 'present'. Can be null. |  dict |
