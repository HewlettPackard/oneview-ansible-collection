## oneview_storage_volume_attachment_facts
Retrieve facts about the OneView Storage Volume Attachments.

#### Synopsis
 Retrieve facts about the OneView Storage Volume Attachments. To gather facts about a specific Storage Volume Attachment it is required to inform the option _storageVolumeAttachmentUri_. It is also possible to retrieve a specific Storage Volume Attachment by the Server Profile and the Volume. For this option, it is required to inform the option _serverProfileName_ and the param _storageVolumeName_ or _storageVolumeUri_.

#### Requirements (on the host that executes the module)
  * python >= 2.7.9
  * hpeOneView >= 5.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| options  |   No  |  | |  Retrieve additional facts. Options available: `extraUnmanagedStorageVolumes` retrieve the list of extra unmanaged storage volumes. `paths` retrieve all paths or a specific attachment path for the specified volume attachment. To retrieve a specific path a `pathUri` or a `pathId` must be informed  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |
| serverProfileName  |   No  |  | |  Server Profile name.  |
| storageVolumeAttachmentUri  |   No  |  | |  Storage Volume Attachment uri.  |
| storageVolumeName  |   No  |  | |  Storage Volume name.  |
| storageVolumeUri  |   No  |  | |  Storage Volume uri.  |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_storage_volume_attachment_facts
```

## License

Apache

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| extra_unmanaged_storage_volumes   | Has facts about the extra unmanaged storage volumes. |  When requested, but can be null. |  dict |
| storage_volume_attachment_paths   | Has facts about all paths or a specific attachment path for the specified volume attachment. |  When requested, but can be null. |  dict |
| storage_volume_attachments   | Has all the OneView facts about the Storage Volume Attachments. |  Always, but can be null. |  dict |