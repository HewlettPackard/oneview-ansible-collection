## oneview_hypervisor_cluster_profile
Manage OneView Hypervisor Cluster Profile resources.

#### Synopsis
 Provides an interface to manage Hypervisor Cluster Profile resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional and when used should be present in the host running the ansible commands. If the file path is not provided, the configuration will be loaded from environment variables. For links to example configuration files or how to use the environment variables verify the notes section.  |
| data  |   Yes  |  | |  List with the Hypervisor Cluster Profile properties.  |
| params  |     |  | |  force flag  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Hypervisor Cluster Profile resource. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_hypervisor_cluster_pofile
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| hypervisor_cluster_pofile  | Has the facts about the managed OneView Hypervisor CLuster Profile. |  On state 'present'. Can be null. |  dict |
