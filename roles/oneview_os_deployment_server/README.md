## oneview_scope
Manage OneView OS Deployment Server resources.

#### Synopsis
 Provides an interface to manage OS Deployment Server resource. Can create, update, or delete OneView OS Deployment Server resources.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the OS Deployment Server properties.  |
| state  |  Yes |  | <ul> <li>present</li>  <li>absent</li>  </ul> |  Indicates the desired state for the resource. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_os_deployment_server
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| oneview_os_deployment_server   | Has the facts about the OS Deployment Server resources |  On state 'present' but can be null. |  dict |
