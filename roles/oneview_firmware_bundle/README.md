## oneview_firmware_bundle
Provides an interface to upload Firmware Bundle resources.

#### Synopsis
 Provides an interface to upload Firmware Bundle resources.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.3.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   No  |  | |  List with the Firmware Bundle properties.  |
| name  |   No  |  | |  Firmware Bundle name.  |
| state  |  Yes |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Firmware Bundle. `present` will ensure data properties are compliant with OneView.|


## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_firmware_bundle
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| firmware_bundle   | Has the facts about the managed OneView Firmware Bundle. |  On state 'present'. Can be null. |  dict |
| compsig      | Has the facts about the signature of OneView Firmware Bundle. |  On state 'add_signature'.        |  dict |
