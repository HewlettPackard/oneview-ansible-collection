## image_streamer_build_plan
Manage the OS build plan resource.

#### Synopsis
 Manage the OS build plan resource.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with OS Build Plan properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the OS Build Plan resource. `present` will ensure data properties are compliant with Synergy Image Streamer. `absent` will remove the resource from Synergy Image Streamer, if it exists.  |


## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.image_streamer_build_plan
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| build_plan   | Has the OS build plan. |  Always. Cannot be null. |  dict |
