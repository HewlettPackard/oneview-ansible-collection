## oneview_storage_volume_template
Manage OneView Storage Volume Template resources.

#### Synopsis
 Provides an interface to manage Storage Volume Template resources. Can create, update and delete.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Storage Volume Template properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Storage Volume Template resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_volume_template
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_volume_template   | Has the OneView facts about the Storage Volume Template. |  On 'present' state, but can be null. |  dict |