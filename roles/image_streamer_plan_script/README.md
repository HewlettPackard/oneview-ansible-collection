## image_streamer_plan_script
Manage the Plan Script resources.

#### Synopsis
 Manage the Plan Script resources.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>differences_retrieved</li> </ul> |  Indicates the desired state for the resource. `present` will ensure data properties are compliant with appliance. `absent` will remove the resource, if it exists. `differences_retrieved` retrieve the Plan Script content differences |
| data  |  No  |  | | List with the Plan Scripts properties.

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.image_streamer_plan_script
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| plan_script   | Has the facts about the Image Streamer Plan Script. |  On state 'present', but can be null. |  dict |
| plan_script_differences   | Has the Plan Script content differences. |  Always. Cannot be null. |  dict |