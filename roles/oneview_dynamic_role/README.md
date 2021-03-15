## oneview_dynamic_role
Manage multiple Oneview resources.

#### Synopsis
 Provides an interface to manage multiple Oneview resources.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.5.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Fibre Channel Network properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Fibre Channel Network resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_dynamic_role
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| ethernet_network   | Has the facts about the managed OneView ethernet Network. |  On state 'present'. Can be null. |  dict |
| fc_network    | Has the facts about the managed OneView FC Network. |  On state 'present'. Can be null. |  dict |
