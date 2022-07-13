## oneview_appliance_time_and_locale_configuration
Manage the OneView Appliance Time and Locale Configuration resources.

#### Synopsis
 Configures the OneView Appliance time and locale settings.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |  Yes  |  | |  List with time and locale settings properties and its associated states.

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_time_and_locale_configuration
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_time_and_locale_configuration   | Has all the OneView facts about the appliance time and locale configuration. |  On 'present' state. Cannot be null. |  dict |
