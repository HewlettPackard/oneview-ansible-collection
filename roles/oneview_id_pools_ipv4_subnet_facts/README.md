## oneview_id_pools_ipv4_subnet_facts
Manage OneView ID Pools IPv4 subnet resources.

#### Synopsis
Provides an interface to retrieve facts about ID Pools IPv4 Subnet Facts resources.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| networkId  |   |  | |  IPv4 Subnet Network ID.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_id_pools_ipv4_subnet_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| id_pools_ipv4_subnets  | Has the facts about the managed OneView ID Pools IPv4 Subnet |  On state 'present'. Can be null. |  dict |
