## oneview_version_facts
Returns the range of possible API versions supported by the appliance

#### Synopsis
 Provides an interface to return the range of possible API versions supported by the appliance.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.4.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| params  |   No  |  | |  List of params to delimit, filter and sort the list of resources.  params allowed: `start`: The first item to return, using 0-based indexing. `count`: The number of resources to return. `filter`: A general filter/query string to narrow the list of items returned. `sort`: The sort order of the returned data set.  |

#### Example Playbook

```yaml

- name: Gather facts about current and minimum Version
  oneview_version_facts:
    config: "{{ config_file_path }}"

- debug: var=version

```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| version   | Has the facts about the OneView current and minimum version. |  When requested, but can not be null |  dict |
