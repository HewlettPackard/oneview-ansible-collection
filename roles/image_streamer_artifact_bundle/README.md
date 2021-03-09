## image_streamer_artifact_bundle
Manage the Artifact Bundle resource.

#### Synopsis
 Provides an interface to manage the Artifact Bundle. Can create, update, remove, and download, upload, extract

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with Artifact Bundle properties and its associated states.  |
| state  |   Yes  |  | <ul> <li>present</li>  <li>absent</li>  <li>downloaded</li>  <li>archive_downloaded</li>  <li>backup_uploaded</li>  <li>backup_created</li>  <li>extracted</li>  <li>backup_extracted</li> </ul> |  Indicates the desired state for the Artifact Bundle resource. `present` will ensure data properties are compliant with OneView. When the artifact bundle already exists, only the name is updated. Changes in any other attribute value is ignored. `absent` will remove the resource from OneView, if it exists. `downloaded` will download the Artifact Bundle to the file path provided. `archive_downloaded` will download the Artifact Bundle archive to the file path provided. `backup_uploaded` will upload the Backup for the Artifact Bundle from the file path provided. `backup_created` will create a Backup for the Artifact Bundle. `extracted` will extract an Artifact Bundle. `backup_extracted` will extract an Artifact Bundle from the Backup.  |



#### Example playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.image_streamer_artifact_bundle
```

## License

Apache


#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| artifact_bundle   | Has the OneView facts about the Artifact Bundles. |  On state 'present' and 'extracted'. |  dict |
| artifact_bundle_deployment_group   | Has the OneView facts about the Deployment Group. |  On state 'backup_extracted', 'backup_uploaded', and 'backup_created'. |  dict |
