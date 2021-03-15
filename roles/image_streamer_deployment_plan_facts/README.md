## image_streamer_deployment_plan_facts
Retrieve facts about the Image Streamer Deployment Plans.

#### Synopsis
 Retrieve facts about one or more of the Image Streamer Deployment Plans.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| name  |   No  |  | |  Deployment Plan name.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |
| options  |   No  |  | |  List with options to gather additional facts about Deployment Plan related resource. Options allowed: `usedby`, `osdp`  |


## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.image_streamer_deployment_plan_facts
```

## License

Apache


#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| deployment_plans   | The list of Deployment Plans. |  Always, but can be null. |  list |
