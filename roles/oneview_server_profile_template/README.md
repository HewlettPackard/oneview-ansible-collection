## oneview_server_profile_tempalte
Manage OneView Server Profile Template resources.

#### Synopsis
 Provides an interface to manage Server Profile Template. Can create, update, or delete Server Profile Template.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the  Server Profile Template properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>resource_assignments_updated</li> </ul> |  Indicates the desired state for the Scope resource. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists. `resource_assignments_updated` modifies scope membership by adding or removing resource assignments. This operation is non-idempotent.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_server_profile_tempalte
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
|  Server Profile Template  | Has the facts about the Server Profile Template. |  On state 'present' and 'resource_assignments_updated', but can be null. |  dict |
