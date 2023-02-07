## oneview_sas_logical_jbod
Manage SAS logical JBOD resources.

#### Synopsis
Provides an interface to manage SAS logical JBOD resources. Can refresh and do patch operations.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with JBOD properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> <li>change_name</li> <li>change_description</li> <li>erase_data</li> <li>clear_metadata</li></ul> |  Indicates the desired state for the SAS logical JBOD resource. `present` will create the resource. `absent` will delete the resource. `change_name` will change the name of the resource. `change_description` will change the description of the resource. `erase_data` will disable drive sanitize option. `clear_metadata` will clear the meta data. |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_sas_logical_jbod
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_logical_jbod   | Has the facts about the SAS logical JBOD. |  On all available states. Can be null. |  dict |
