## oneview_storage_pool_facts
Retrieve facts about one or more Storage Pools.

#### Synopsis
 Retrieve facts about one or more of the Storage Pools from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.8.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Storage Pool name.  |
| options  |   No  |  | |  List with options to gather additional facts about Storage Pools. Options allowed: `reachableStoragePools` gets the list of reachable Storage pools based on the network param. If the network param is not specified it gets all of them.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_pool_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_pools   | Has all the OneView facts about the Storage Pools. |  Always, but can be null. |  dict |
| storage_pools_reachable_storage_pools   | Has all the OneView facts about the Reachable Storage Pools. |  Always, but can be null. |  dict |