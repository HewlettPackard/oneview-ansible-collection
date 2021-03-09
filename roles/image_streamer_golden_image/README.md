## image_streamer_golden_image
Manage the Golden Image resource.

#### Synopsis
 Manage the Golden Image resource.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li>  <li>archive_downloaded</li>  <li>downloaded</li> |  Indicates the desired state for the resource. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists. `archive_downloaded` Download the Golden Image archive log to the file path provided. `downloaded` Download the Golden Image to the file path provided  |
| data  |  No  |  | | List with the Golden Image properties.
| params  |  No  |  | | List of params to filter and sort the list of resources. params allowed: start: The first item to return, using 0-based indexing. count: The number of resources to return. filter: A general filter/query string to narrow the list of items returned. sort: The sort order of the returned data set.

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.image_streamer_golden_image
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| os_volume_name   | Has the name of OS volume. |  Always. Can be null. |  str |
| build_plan_name  | Has the name of build plan. | Always. Can be null. |  str |