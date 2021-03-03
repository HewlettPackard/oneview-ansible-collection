## appliance_device_snmp_v3_users_facts
Retrieve the facts about one or more of the OneView SNMP V3 Users.

#### Synopsis
 Retrieve the facts about one or more of the SNMP V3 Users from OneView.

#### Requirements (on the host that executes the module)
  * hpeOneView >=6.0.0  

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional and when used should be present in the host running the ansible commands. If the file path is not provided, the configuration will be loaded from environment variables. For links to example configuration files or how to use the environment variables verify the notes section.  |
| name  |   No  |  | |  SNMP V3 Users name.  |
| options  |   No  |  | |  SNMP V3 Users compliance.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `sort`: The sort order of the returned data set.  |
## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_appliance_device_snmp_v3_users_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| appliance_device_snmp_v3_users_facts   | Has all the OneView facts about the Hypervsior Cluster Profile. |  Always, but can be null. |  dict |
