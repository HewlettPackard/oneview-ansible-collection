## oneview_hypervisor_manager
Manage OneView Hypervisor Manager resources.

#### Synopsis
 Provides an interface to manage Hypervisor Manager resources. Can create, update, or delete.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0
  * python >= 2.7.9

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional and when used should be present in the host running the ansible commands. If the file path is not provided, the configuration will be loaded from environment variables. For links to example configuration files or how to use the environment variables verify the notes section.  |
| data  |   Yes  |  | |  List with the Hypervisor Manager properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Hypervisor Manager resource. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_hypervisor_manager
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| hypervisor_managers   | Has all the OneView facts about the Hypervisor Managers. |  Always, but can be null. |  dict |
