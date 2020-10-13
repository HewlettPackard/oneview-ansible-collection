## oneview_certificates_server_facts
Retrieve the facts about one or more of the OneView Certificates Server.

#### Synopsis
 Retrieve the facts about one or more of the Certificates Server from OneView.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0
  * python >= 2.7.9

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional and when used should be present in the host running the ansible commands. If the file path is not provided, the configuration will be loaded from environment variables. For links to example configuration files or how to use the environment variables verify the notes section.  |
| aliasName  |   No  |  | |  Certificates Server aliasName.  |
| remote  |   No  |  | |  Remote Server Certificate.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_certificate_server_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| certificates_servers   | Has all the OneView facts about the Certificates Server. |  Always, but can be null. |  dict |
| remote_certificate     | Has facts about remote server certificates               |  When required            |  dict |