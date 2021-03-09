## image_streamer_plan_script_facts
Retrieve facts about Plan Scripts resource.

#### Synopsis
 Retrieve facts about Plan Scripts resource.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| options  |   No  |  | |  plan scripts compliance.  |
| params  |  No  |  | | List of params to filter and sort the list of resources. params allowed: start: The first item to return, using 0-based indexing. count: The number of resources to return. filter: A general filter/query string to narrow the list of items returned. sort: The sort order of the returned data set.  |

## Example Playbook
 
```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.image_streamer_plan_script_facts
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| plan_scripts   | Has all the facts about the plan scripts. |  Always. Cannot be null. |  dict |
| use_by  | Has all the facts about the build plans of given plan script.| Always. Cannot be null. |  dict |