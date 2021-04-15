## oneview_appliance_device_read_community
Manage the Appliance Device Read Community string.

#### Synopsis
 Provides an interface to manage the Appliance Device Read Community string. It can only update it. This results in an update of the community string on all servers being managed/monitored by this OneView instance. The supported characters for community string are aA-zA, 0-9, !, ",

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the Appliance Device Read Community.  |
| state  |   |  | <ul> <li>present</li> </ul> |  Indicates the desired state for the Appliance Device Read Community. `present` ensures data properties are compliant with OneView.  |


## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_device_read_community
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_device_read_community   | Has all the OneView facts about the OneView Appliance Device Read Community. |  Always. |  dict |