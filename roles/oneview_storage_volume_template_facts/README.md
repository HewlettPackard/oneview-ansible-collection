## oneview_storage_volume_template_facts
Retrieve facts about Storage Volume Templates of the OneView.

#### Synopsis
Retrieve facts about Storage Volume Templates of the OneView.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Storage Volume Template name.  |
| options  |   No  |  | |  Retrieve additional facts. Options available: `connectableVolumeTemplates`, `reachableVolumeTemplates`, `compatibleSystems`  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_volume_template_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| compatible_systems   | Has facts about Storage Systems compatible to the Storage Volume template. API version 500+ only. |  When requested, but can be null. |  dict |
| connectable_volume_templates   | Has facts about the Connectable Storage Volume Templates. API version <= 300  only. |  When requested, but can be null. |  dict |
| reachable_volume_templates   | Has facts about the Reachable Storage Volume Templates. API version 500+ only. |  When requested, but can be null. |  dict |
| storage_volume_templates   | Has all the OneView facts about the Storage Volume Templates. |  Always, but can be null. |  dict |
