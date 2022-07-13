## image_streamer_deployment_plan
Manage Image Streamer Deployment Plan resources.

#### Synopsis
 Provides an interface to manage Image Streamer Deployment Plans. Can create, update, and remove.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Deployment Plan properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  Indicates the desired state for the Deployment Plan resource. `present` will ensure data properties are compliant with Synergy Image Streamer. `absent` will remove the resource from Synergy Image Streamer, if it exists.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.image_streamer_deployment_plan
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| deployment_plan   | Has the facts about the Image Streamer Deployment Plan. |  On state 'present', but can be null. |  dict |
