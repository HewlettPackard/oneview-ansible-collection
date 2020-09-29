[![Build Status](https://travis-ci.org/HewlettPackard/oneview-ansible.svg?branch=master)](https://travis-ci.org/HewlettPackard/oneview-ansible)
[![Coverage Status](https://coveralls.io/repos/github/HewlettPackard/oneview-ansible/badge.svg?branch=master)](https://coveralls.io/github/HewlettPackard/oneview-ansible?branch=master)

# Ansible Modules for HPE OneView

Modules to manage HPE OneView using Ansible collection framework.

## Requirements

 - Ansible >= 2.9
 - Python >= 3.4.2
 - HPE OneView Python SDK

# Installation
```bash
ansible-galaxy collection install hpe.oneview
```

To perform a full installation, you should execute the following steps:

### 1. Install dependency packages

Run pip command from the cloned directory:
    
  ```bash
  pip install -r requirements.txt
  ```

### 2. Install ansible
    
  ```bash
  apt-get -y update
  apt-get install ansible
  ```
  
### 3. Configure the ANSIBLE_LIBRARY environmental variable

Set the environment variables `ANSIBLE_LIBRARY` and `ANSIBLE_MODULE_UTILS`, specifying the `library` full path from the cloned project:

```bash
$ export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
$ export ANSIBLE_MODULE_UTILS=/path/to/oneview-ansible/library/module_utils/
```

### 4. OneViewClient Configuration

#### Using a JSON Configuration File

To use the Ansible OneView modules, you can store the configuration on a JSON file. This file is used to define the
settings, which will be used on the OneView appliance connection, like hostname, username, and password. Here's an
example:

```json
{
  "ip": "172.25.105.12",
  "credentials": {
    "userName": "Administrator",
    "authLoginDomain": "",
    "password": "secret123"
  },
  "api_version": 2000
}
```

The `api_version` specifies the version of the Rest API to invoke. When not defined, it will use `300` as the
default value.

If your environment requires a proxy, define the proxy properties in the JSON file using the following syntax:

```json
  "proxy": "<proxy_host>:<proxy_port>"
```

:lock: Tip: Check the file permissions since the password is stored in clear-text.

The configuration file path must be provided for all of the playbooks `config` arguments. For example:

```yml
- name: Gather facts about the FCoE Network with name 'FCoE Network Test'
  oneview_fcoe_network_facts:
    config: "/path/to/config.json"
    name: "FCoE Network Test"
```

#### Environment Variables

If you prefer, the configuration can also be stored in environment variables.

```bash
# Required
export ONEVIEWSDK_IP='172.25.105.12'
export ONEVIEWSDK_USERNAME='Administrator'
export ONEVIEWSDK_PASSWORD='secret123'

# Optional
export ONEVIEWSDK_API_VERSION='200'
export ONEVIEWSDK_AUTH_LOGIN_DOMAIN='authdomain'
export ONEVIEWSDK_PROXY='<proxy_host>:<proxy_port>'
```

:lock: Tip: Make sure no unauthorised person has access to the environment variables, since the password is stored in clear-text.

In this case, you shouldn't provide the `config` argument. For example:

```yml
- name: Gather facts about the FCoE Network with name 'FCoE Network Test'
  oneview_fcoe_network_facts:
    name: "FCoE Network Test"
```

Once you have defined the environment variables, you can run the roles.

#### Parameters in roles

The third way to pass in your HPE OneView credentials to your tasks is through explicit specification on the task.

This option allows the parameters `hostname`, `username`, `password`, `api_version` and `image_streamer_hostname` to be passed directly inside your task.

```yaml
- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 2000
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

### 5. Setting your OneView version

The Ansible modules for HPE OneView support the API endpoints for HPE OneView 4.00, 4.10, 4.20, 5.00, 5.20, 5.30, 5.40

The current `default` HPE OneView version will pick the OneView appliance version.

To use a different API, you must set the API version together with your credentials, either using the JSON configuration:

```json
"api_version": 2000
```
OR using the Environment variable:

```bash
export ONEVIEWSDK_API_VERSION='2000'
```

If this property is not specified, it will fall back to efault value.

The API list is as follows:

- HPE OneView 4.00 API version: `600`
- HPE OneView 4.10 API version: `800`
- HPE OneView 4.20 API version: `1000`
- HPE OneView 5.00 API version: `1200`
- HPE OneView 5.20 API version: `1600`
- HPE OneView 5.30 API version: `1800`
- HPE OneView 5.40 API version: `2000`

### 6. HPE Synergy Image Streamer

Modules to manage HPE Synergy Image Streamer appliances are also included in this project.
To use these modules, you must set the Image Streamer IP on the OneViewClient configuration,
either using the JSON configuration:

```json
"image_streamer_ip": "100.100.100.100"
```

OR using the Environment variable:

```bash
export ONEVIEWSDK_IMAGE_STREAMER_IP='100.100.100.100'
```

You can find sample playbooks in the [examples](https://github.com/HewlettPackard/oneview-ansible/tree/master/examples) folder. Just look for the playbooks with the ```image_streamer_``` prefix.


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

© Copyright 2020 Hewlett Packard Enterprise Development LP
