## image_streamer_golden_image_facts
Retrieve facts about the golden images resource.

#### Synopsis
 Retrieve facts about the golden images resource.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| params  |  No  |  | | List of params to filter and sort the list of resources. params allowed: start: The first item to return, using 0-based indexing. count: The number of resources to return. filter: A general filter/query string to narrow the list of items returned. sort: The sort order of the returned data set.

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.image_streamer_golden_image_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| golden_images   | Has all facts about golden image resource. |  Always. Can be null. |  dict |
