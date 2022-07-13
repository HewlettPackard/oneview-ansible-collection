# Ansible Collection for HPE OneView

This collection provides a series of Ansible modules and plugins for interacting with the HPE OneView Modules.

## Build Status 

OV Version | 7.00 | 6.60 | 6.50 | 6.40 | 6.30 | 6.20 | 6.10 | 6.00 | 5.60 | 
| -------------:|-------------:| -------------:| -------------:|:-------------:| -------------:| -------------:| -------------:| -------------:| -------------:|
SDK Version/Tag | [v7.0.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v7.0.0)| [v6.6.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v6.6.0)| [v6.5.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v6.5.0)| [v6.4.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v6.4.0) | [v6.3.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v6.3.0) | [v6.2.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v6.2.0) | [v6.1.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v6.1.0) | [v6.0.0](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v6.0.0) | [v1.2.1](https://github.com/HewlettPackard/oneview-ansible-collection/releases/tag/v1.2.1) |
Build Status | [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/2306414699)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/2021346524)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/1666302716)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/1474959987)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/1208451472)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/1025475033)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/728874027)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/runs/632343827)| [![Build status](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml/badge.svg)](https://github.com/HewlettPackard/oneview-ansible-collection/actions/workflows/.ansible-test.yml)|


## Requirements

 - Ansible >= 2.9
 - python >= 3.4.2
 - [HPE OneView Python SDK](https://pypi.org/project/hpeOneView/)

# Installation
To install HPE OneView collection hosted in Galaxy

```bash
ansible-galaxy collection install hpe.oneview
```

To upgrade to the latest version of HPE OneView:

```bash
ansible-galaxy collection install hpe.oneview --force
```

To install dependency packages

```bash
pip install -r ~/.ansible/collections/ansible_collections/hpe/oneview/requirements.txt
```

To install HPE OneView collection from GitHub
```bash
git clone https://github.com/HewlettPackard/oneview-ansible-collection.git
cd oneview-ansible-collection
ansible-galaxy collection build .
```
Now a tar file is generated. Install that file.
```
ansible-galaxy collection install <tar_file>
```

To install dependency packages
    
```bash
pip install -r requirements.txt
```
To install HPE OneView collection from Docker Image

```bash
docker build -t oneview-ansible-collections .
docker run -it --rm -v (pwd)/:/root/oneview-ansible-collections oneview-ansible-collections
```
That's it. If you would like to modify any role, simply modify role and re-run the image.

###  OneViewClient Configuration

#### Using a JSON Configuration File

To use the HPE OneView collection, you can store the configuration in a JSON file. This file is used to define the
settings, which will be used on the OneView appliance connection, like hostname, authLoginDomain, username, and password. Here's an
example:

```json
{
  "ip": "<ip>",
  "credentials": {
    "userName": "<userName>",
    "authLoginDomain": "",
    "password": "<password>"
  },
  "api_version": 4000
}
```

The `api_version` specifies the version of the Rest API to invoke. When not defined, it will pick 
the OneView appliance version as `default`.

The `authLoginDomain` specifies the login domain directory of the appliance. When it is not specified, 
it will consider the appliance's default domain directory.

If your environment requires a proxy, define the proxy properties in the JSON file using the following syntax:

```json
  "proxy": "<proxy_host>:<proxy_port>"
```

:lock: Tip: Check the file permissions since the password is stored in clear-text.

The configuration file path must be provided for all of the roles `config` arguments. For example:

```yml
- name: Gather facts about the FCoE Network with name 'FCoE Network Test'
  oneview_fcoe_network_facts:
    config: "/path/to/config.json"
    name: "FCoE Network Test"
```

Once you have defined the config variables, you can run the roles.

#### Pass Login SessionID as param

To run any task, we first need to login to HPE OneView appliance by passing the credentials in form of configuration. As part of the login process, Ansible Collection SDK gets the session id from OneView and individual sessionID is generated for each task. This could cause a session limit exceeded issue if there are more number of tasks.

So it is recommended to use a single sessionID for all tasks. But it is optional. If sessionID is not passed explicitly, it will work as earlier.

To reuse a single sessionID, it has to be passed as param `sessionID` inside your task.

Here's an 
example:

```yaml
- name: Fetch Session Id
  oneview_get_session_id:
    config: "{{ config }}"
    name: "Test_Session"
  delegate_to: localhost
  register: session

- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: <hostname>
    username: <username>
    password: <password>
    auth_login_domain: <domain_directory>
    api_version: 4000
    sessionID: "{{ session.ansible_facts.session }}"
    state: present
    data:
      name: "{{ network_name }}"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
  no_log: true
  delegate_to: localhost
```

A SessionID remains valid for 24 hours.

#### Parameters in roles

The another way is to pass in your HPE OneView credentials to your tasks is through explicit specification on the task.

This option allows the parameters `hostname`, `auth_login_domain`, `username`, `password`, `api_version` and `image_streamer_hostname` to be passed directly inside your task.

```yaml
- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: <hostname>
    username: <username>
    password: <password>
    auth_login_domain: <domain_directory>
    api_version: 4000
    state: present
    data:
      name: "{{ network_name }}"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
  no_log: true
  delegate_to: localhost
```

Setting `no_log: true` is highly recommended in this case, as the credentials are otherwise returned in the log after task completion.

### Setting your OneView version

The Ansible collections for HPE OneView support the API endpoints for HPE OneView  6.00, 6.10, 6.20, 6.30, 6.40, 6.50, 6.60, 7.00

The current `default` HPE OneView version will pick the OneView appliance version.

To use a different API, you must set the API version together with your credentials, either using the JSON configuration:

```json
"api_version": 4000
```
OR using the Environment variable:

```bash
export ONEVIEWSDK_API_VERSION='4000'
```

If this property is not specified, it will fall back to default value.

The API list is as follows:

- HPE OneView 5.60 API version: `2400`
- HPE OneView 6.00 API version: `2600`
- HPE OneView 6.10 API version: `2800`
- HPE OneView 6.20 API version: `3000`
- HPE OneView 6.30 API version: `3200`
- HPE OneView 6.40 API version: `3400`
- HPE OneView 6.50 API version: `3600`
- HPE OneView 6.60 API version: `3800`
- HPE OneView 7.00 API version: `4000`

### HPE Synergy Image Streamer

Modules to manage HPE Synergy Image Streamer appliances are also included in this project.
To use these modules, you must set the Image Streamer IP on the OneViewClient configuration,
either using the JSON configuration:

```json
"image_streamer_ip": "<image_streamer_ip>"
```

OR using the Environment variable:

```bash
export ONEVIEWSDK_IMAGE_STREAMER_IP='100.100.100.100'
```

### Usage

Playbooks

To use a module from HPE OneView collection, please reference the full namespace, collection name, and modules name that you want to use:

```bash
---
- name: Using HPE OneView collection
  hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_fc_network
    - hpe.oneview.oneview_fc_network_facts
  ```

Run the above created playbooks as shown below.

```bash   
ansible-playbook example_collection.yml
```

## License

This project is licensed under the Apache 2.0 license. Please see the [LICENSE](LICENSE) for more information.

## Contributing and feature requests

**Contributing:** We welcome your contributions to the Ansible Modules for HPE OneView. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

**Feature Requests:** If you have a need that is not met by the current implementation, please let us know (via a new issue).
This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought of everything, because we assure you that is not the case.

## Features

The HPE.Oneview collection includes
[roles](https://github.com/HewlettPackard/oneview-ansible-collection/tree/master/roles/),
[modules](https://github.com/HewlettPackard/oneview-ansible-collection/tree/master/plugins/modules),
[sample playbooks](https://github.com/HewlettPackard/oneview-ansible-collection/tree/master/playbooks),
[module_utils](https://github.com/HewlettPackard/oneview-ansible-collection/tree/master/plugins/module_utils)


## Copyright

© Copyright 2021 Hewlett Packard Enterprise Development LP
