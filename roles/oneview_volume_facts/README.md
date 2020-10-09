## oneview_volume_facts
Retrieve facts about the OneView Volumes.

#### Synopsis
 Retrieve facts about the Volumes from OneView.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.8.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Volume name.  |
| options  |   No  |  | |  List with options to gather additional facts about Volume and related resources. Options allowed: - `attachableVolumes` - `extraManagedVolumePaths` - `snapshots`. For this option, you may provide a name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_volume_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| attachable_volumes   | Has all the facts about the attachable volumes managed by the appliance. |  When requested, but can be null. |  dict |
| extra_managed_volume_paths   | Has all the facts about the extra managed storage volume paths from the appliance. |  When requested, but can be null. |  dict |
| storage_volumes   | Has all the OneView facts about the Volumes. |  Always, but can be null. |  dict |
