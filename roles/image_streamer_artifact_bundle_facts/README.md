## image_streamer_artifact_bundle_facts
Retrieve facts about the Artifact Bundle.

#### Synopsis
 Retrieve facts about the Artifact Bundle.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the Artifact Bundle.  |
| options  |   No  |  | |  List with options to gather additional facts about the Artifact Bundle. Options allowed: `allBackups` gets the list of backups for the Artifact Bundles. `backupForAnArtifactBundle` gets the list of backups for the Artifact Bundle.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


#### Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.image_streamer_artifact_bundle_facts
```

## License

Apache


#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| artifact_bundle_backups   | The list of backups for the Artifact Bundles. |  When requested, but can also be null. |  list |
| artifact_bundles   | The list of Artifact Bundles. |  Always, but can be also null. |  list |
