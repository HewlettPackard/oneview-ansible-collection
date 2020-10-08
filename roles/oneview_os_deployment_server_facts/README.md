## oneview_os_deployment_facts
Manage OneView Oneview OS Deployment Server Facts resources.

#### Synopsis
 Provides an interface to manage Oneview OS Deployment Server Facts.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the OS Deployment Server properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  </ul> |  Indicates the desired state for the resource. `present` ensures data properties are compliant with OneView. `absent` removes the resource from OneView, if it exists.
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_os_deployment_server_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
|  OS Deployment Server  | Has the facts about the  OS Deployment Server. |  On state 'present' can be null. |  dict |
