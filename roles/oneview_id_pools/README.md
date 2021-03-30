## oneview_id_pools
Manage OneView ID Pools resources.

#### Synopsis
 Provides an interface to manage ID Pools resources. Can create, update, and delete.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the ID Pool properties.  |
| state  |   |  | <ul> <li>allocate</li>  <li>collect</li> </ul> |  Indicates the desired state for the resource. `allocate` will reserve set of Ids. `collect` will gather the allocated Ids.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_id_pools
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| id_pools | Has the facts about the managed OneView ID Pools |  On state 'collect'. Can be null. |  dict |
