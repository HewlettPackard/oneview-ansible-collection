## oneview_interconnect_facts
Retrieve facts about one or more of the OneView Interconnects.

#### Synopsis
 Retrieve facts about one or more of the Interconnects from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.8.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Interconnect name.  |
| options  |   No  |  | |  List with options to gather additional facts about Interconnect. Options allowed: `nameServers` gets the named servers for an interconnect. `statistics` gets the statistics from an interconnect. `portStatistics` gets the statistics for the specified port name on an interconnect. `subPortStatistics` gets the subport statistics on an interconnect. `ports` gets all interconnect ports. `port` gets a specific interconnect port. `pluggableModuleInformation` gets all the SFP information.  To gather additional facts it is required inform the Interconnect name. Otherwise, these options will be ignored.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_interconnect_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| interconnect_name_servers   | The named servers for an interconnect. |  When requested, but can be null. |  list |
| interconnect_pluggable_module_information   | The plugged SFPs information. |  When requested, but can be null. |  list |
| interconnect_port   | The interconnect port. |  When requested, but can be null. |  dict |
| interconnect_port_statistics   | Statistics for the specified port name on an interconnect. |  When requested, but can be null. |  dict |
| interconnect_ports   | All interconnect ports. |  When requested, but can be null. |  list |
| interconnect_statistics   | Has all the OneView facts about the Interconnect Statistics. |  When requested, but can be null. |  dict |
| interconnect_subport_statistics   | The subport statistics on an interconnect. |  When requested, but can be null. |  dict |
| interconnects   | The list of interconnects. |  Always, but can be null. |  list |
