## oneview_firmware_driver
Provides an interface to remove Firmware Driver resources.

#### Synopsis
 Provides an interface to remove Firmware Driver resources.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   No  |  | |  List with the Firmware Driver properties.  |
| name  |   No  |  | |  Firmware driver name.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Firmware Driver. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_firmware_driver
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| firmware_driver   | Has the facts about the managed OneView Firmware Driver. |  On state 'present'. Can be null. |  dict |
