## oneview_appliance_configuration_timeconfig_facts
Retrieve facts about the OneView Time Configuration.

#### Synopsis
 Retrieve facts about the OneView Time Configuration.

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
    - hpe.oneview.oneview_appliance_configuration_timeconfig
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_configuration_timeconfig   | Has all the OneView facts about the supported appliance locales. |  Always. Cannot be null. |  dict |
