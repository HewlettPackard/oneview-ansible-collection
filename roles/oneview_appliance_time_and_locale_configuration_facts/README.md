## oneview_appliance_time_and_locale_configuration_facts
Retrieve facts about the OneView Appliance Time and Locale Configuration.

#### Synopsis
 Retrieve facts about the OneView Appliance time and locale information.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.6.0

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
    - hpe.oneview.oneview_appliance_time_and_locale_configuration_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_time_and_locale_configuration   | Has all the OneView facts about the appliance time and locale configuration. |  Always. Cannot be null. |  dict |
