## oneview_volume
Manage OneView Volume resources.

#### Synopsis
 Provides an interface to manage Volume resources. It allows create, update, delete or repair the volume, and create or delete a snapshot.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  Volume or snapshot data.  |
| export_only  |   |  False  | |  If set to True, when the status is `absent` and the resource exists, it will be removed only from OneView.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>repaired</li>  <li>snapshot_created</li>  <li>snapshot_deleted</li> </ul> |  Indicates the desired state for the Volume resource. `present` creates/adds the resource when it does not exist, otherwise it updates the resource. When the resource already exists, the update operation is non-convergent, since it is always called even though the given options are compliant with the existent data. To change the name of the volume, a `newName` in the _data_ must be provided. `absent` by default deletes a volume from OneView and the storage system. When export_only is True, the volume is removed only from OneView. `repaired` removes extra presentations from a specified volume on the storage system. This operation is non-idempotent. `snapshot_created` creates a snapshot for the volume specified. This operation is non-idempotent. `snapshot_deleted` deletes a snapshot from OneView and the storage system.  |
| validate_etag  |   |  True  | <ul> <li>true</li>  <li>false</li> </ul> |  When the ETag Validation is enabled, the request will be conditionally processed only if the current ETag for the resource matches the ETag provided in the data.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_volume
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| storage_volume   | Has the facts about the Storage Volume. |  On state 'present', but can be null. |  dict |
