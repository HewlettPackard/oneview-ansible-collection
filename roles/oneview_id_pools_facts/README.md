## oneview_id_pools_facts
Manage OneView ID Pools resources.

#### Synopsis
 Provides an interface to manage ID Pools resources. Can get schema, validate, and generate range.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the ID Pool properties.  |
| state  |   |  | <ul> <li>schema</li>  <li>validate</li> </ul> |  Indicates the desired state for the resource. `schema` will fetch Id Pool schema. `validate` will ensure Ids are validated or not.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_id_pools_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| id_pools_facts | Has the facts about the managed OneView ID Pools |  On state 'generate'. Can be null. |  dict |
