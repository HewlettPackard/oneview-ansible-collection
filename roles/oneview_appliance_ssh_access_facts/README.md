## oneview_appliance_ssh_access_facts
Retrieve facts about the OneView Appliance SSH Access.

#### Synopsis
 Retrieve facts about the OneView Appliance SSH Access.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

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
    - hpe.oneview.oneview_appliance_ssh_access_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_ssh_access   | Has all the OneView facts about the appliance SSH access configuration. |  Always. Cannot be null. |  dict |
