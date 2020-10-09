## oneview_storage_volume_attachment
Provides an interface to remove extra presentations from a specified server profile.

#### Synopsis
Provides an interface to remove extra presentations from a specified server profile.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| server_profile  |   Yes  |  | |  Server Profile name or Server Profile URI  |
| state  |   Yes  |  | <ul> <li>extra_presentations_removed</li> </ul> |  Indicates the desired state for the Storage Volume Attachment `extra_presentations_removed` will remove extra presentations from a specified server profile.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_volume_attachment
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| server_profile   | Has all the OneView facts about the repaired Server Profile. |  Always. |  dict |
