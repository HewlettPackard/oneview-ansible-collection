## oneview_interconnect
Manage the OneView Interconnect resources.

#### Synopsis
 Provides an interface to manage Interconnect resources. Can change the power state, UID light state, perform device reset, reset port protection, and update the interconnect ports.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.8.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| ip  |   No  |  | |  Interconnect IP address.  |
| name  |   No  |  | |  Interconnect name.  |
| ports  |   No  |  | |  List with ports to update. This option should be used together with `update_ports` state.  |
| state  |   |  | <ul> <li>powered_on</li>  <li>powered_off</li>  <li>uid_on</li>  <li>uid_off</li>  <li>device_reset</li>  <li>update_ports</li>  <li>reset_port_protection</li>  <li>reconfigured</li> </ul> |  Indicates the desired state for the Interconnect resource. `powered_on` turns the power on. `powered_off` turns the power off. `uid_on` turns the UID light on. `uid_off` turns the UID light off. `device_reset` perform a device reset. `update_ports` updates the interconnect ports. `reset_port_protection` triggers a reset of port protection. `reconfigured` will reapply the appliance's configuration on the interconnect. This includes running the same configuration steps that were performed as part of the interconnect add by the enclosure.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.oneview_interconnect
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect   | Has the facts about the OneView Interconnect. |  Always. Can be null. |  dict |