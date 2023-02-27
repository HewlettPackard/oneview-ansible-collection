## oneview_sas_interconnect
Manage OneView SAS interconnect resources.

#### Synopsis
Provides an interface to manage SAS Interconnect resources. Can refresh and do patch operations.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with SAS Interconnect properties.  |
| state  |   |  | <ul> <li>refreshed</li>  <li>power_on/power_off</li> <li>uid_on/uid_off</li> <li>hard_reset</li> <li>soft_reset</li></ul> |  Indicates the desired state for the SAS interconnect resource. `refreshed` will refresh the SAS interconnect resource. `power_on/power_off` will change the power status. `uid_on/uid_off` will change the uid status. `hard_reset` will hard reset the SAS interconnect. `soft_reset` will soft reset the SAS interconnect. |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_sas_interconnect
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| sas_interconnect   | Has the facts about the SAS Interconnect. |  On all available states. Can be null. |  dict |