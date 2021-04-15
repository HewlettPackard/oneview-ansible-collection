## oneview_appliance_device_read_community_facts
Retrieve the facts about the OneView appliance device read community.

#### Synopsis
 Retrieve the facts about the OneView appliance device read community.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |


## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_device_read_community_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_device_read_community   | Has all the OneView facts about the OneView appliance device read community. |  Always. |  dict |