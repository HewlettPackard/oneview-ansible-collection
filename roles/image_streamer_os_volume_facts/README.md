## image_streamer_os_volume_facts
Retrieve facts about the Image Streamer OS Volumes.

#### Synopsis
 Retrieve facts about the Image Streamer OS Volumes.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Name of the OS Volume.  |
| options  |   No  |  | |  List with options to gather additional facts about OS volumes. Options allowed: `getStorage` gets the storage details of an OS volume `getArchivedLogs` gets the archived logs of an OS volume  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.image_streamer_os_volume_facts
```

## License

Apache


#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| log_file_path   | OS volume archived log file path |   |  str |
| os_volumes   | The list of OS Volumes |  Always, but can be empty. |  list |
| storage   | Storage details of an OS volume. |   |  dict |
