## oneview_hypervisor_cluster_profile_facts
Retrieve the facts about one or more of the OneView Hypervisor Cluster Profiles.

#### Synopsis
 Retrieve the facts about one or more of the Hypervisor Cluster Profiles from OneView.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0  

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional and when used should be present in the host running the ansible commands. If the file path is not provided, the configuration will be loaded from environment variables. For links to example configuration files or how to use the environment variables verify the notes section.  |
| name  |   No  |  | |  Hypervisor Cluster Profile name.  |
| options  |   No  |  | |  Hypervisor Cluster Profile compliance.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `sort`: The sort order of the returned data set.  |
## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_hypervisor_cluster_profile_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| hypervisor_cluster_profile_facts   | Has all the OneView facts about the Hypervsior Cluster Profile. |  Always, but can be null. |  dict |
