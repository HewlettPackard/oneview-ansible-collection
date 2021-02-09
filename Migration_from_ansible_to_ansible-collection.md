# HPE OneView Ansible to Ansible Collection Migration Guide
 
## Preface:
This document helps current customers to move from the legacy Ansible module to the new Ansible collection.
This will enable customers to take full advantage of Infrastructure automation using Ansible Collection Modules, in addition to helping improve the customer experience.
This guide covers various aspects including: Installation of Ansible Collection, Installation of HPE OneView Ansible Collection and running the Ansible playbooks.

This guide also provides step by step details to the Customer for adopting, moving and migrating to OneView-Ansible-collection for each of the below sections.    
* Installation of Ansible Collection
* Installation of HPE OneView Ansible Collection SDK
* Running the Playbooks
* Examples provided in the HPE OneView Ansible Collection
* Conversion of existing custom Ansible Playbooks to Ansible Collection Playbooks.
* Developing New Ansible Collection Playbooks.

## Technical Aspects:
What aspects should I look into / check-list
1. For leveraging HPE OneView Ansible Collection SDK module, the requirement is to have Ansible 2.9 module installed. And uninstall the Ansible module < 2.9 from the DevOps Appliance/OS if exists.
2. Python requirements: Ansible collection works with both Python versions 2.7.9 and 3.6.x. Preferably Python 3.6.x version.
3. The file structure of the Ansible Collection project is different from the Ansible project.
4. Reusable scripts from existing HPE OneView Ansible module:  
   * Python scripts from oneview-ansible/library: Python scripts from Library module are moved to oneview-ansible-collection/plugins/ directory.
   * Tasks scripts from oneview-ansible/examples/ yaml files are moved to oneview-ansible-collection/roles directory

We use the ansible-galaxy executable to create the appropriate collection project structure.
```
    ansible-galaxy collection init oneview_custom_collection_use_case 
```

## Installation of Ansible Collection:

 * As part of using the new Ansible Collection in the DevOps appliance, Customer will need to first uninstall the existing OLD Ansible module if an installed version exists and is < 2.9. 
 * Download and install the Ansible version >= 2.9 from Red Hat portal .
 * HPE OneView Python SDK (https://pypi.org/project/hpeOneView/)

## Installation of HPE OneView Ansible Collection SDK: 
The HPE OneView Ansible Collection includes roles, modules, sample playbooks, module_utils. You can install OneView Ansible Collection modules through multiple ways as listed below.
 * HPE GitHub
 * Ansible Galaxy 
 * Ansible Automation Hub
 * Docker Image

#### Install HPE OneView collection dependency packages:
Please run the below command to install HPE OneView collection dependency packages
```
    $ pip install -r requirements.txt
```

#### Install HPE OneView collection from GitHub:
```
    $ git clone https://github.com/HewlettPackard/oneview-ansible-collection.git
    $ cd oneview-ansible-collection
    $ ansible-galaxy collection build.
```
The build process will create hpe.oneview in tar file format.
```
    $ ansible-galaxy collection install <tar_file>
```

#### Installation HPE OneView Ansible collection from Ansible Galaxy:
The HPE OneView Ansible Collection can be installed using Ansible Galaxy. Content from roles and collections can be referenced in Ansible Playbooks and immediately put to work.
Installing collections with ansible-galaxy is only supported in Ansible version >= 2.9
 
To install HPE OneView collection hosted in Galaxy
```
    $ ansible-galaxy collection install hpe.oneview
```
Please refer to below command for upgrading HPE OneView Collection to the latest version of HPE OneView:
```
    $ ansible-galaxy collection install hpe.oneview –force
```

#### Installation HPE OneView Ansible collection from Red Hat Automation Hub:
The HPE OneView Ansible Collection can be installed using Red Hat Automation Hub. 
Customers may want to leverage Automation Hub for downloading and using the HPE OneView collection module certified by Red Hat. 
At a high level, automation hub provides Ansible certified, supported content by Red Hat and HPE.

Automation hub is available as a Software-as-a-Service (SaaS) offering to existing Red Hat Ansible Automation Platform customers and can be accessed via https://cloud.redhat.com/. 
To consume content from hub as part of your automation workflows can also be accessed via CLI. For this an offline token is required which can be obtained via the web UI at https://cloud.redhat.com/ansible/automation-hub/token.
URL and token needs to be added to the configuration file as follows:

```
    [galaxy]
    server_list = automation_hub, galaxy
    [galaxy_server.automation_hub]
    url=https://cloud.redhat.com/api/automation-hub/
    auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
    token=AABBccddeeff112233gghh
    
    [galaxy_server.galaxy]
    url=https://galaxy.ansible.com/
```

Please refer to below command for installing HPE OneView Collection from the Automation Hub using the above configuration file.
```
    $ ansible-galaxy collection install hpe.oneview:1.0.3
```
Note: Automation Hub supports versioning, enabling users to specify the version. Refer the below link for the steps for automation hub: https://www.ansible.com/blog/getting-started-with-automation-hub

#### Install HPE OneView collection from Docker Image:
The containerized version of the oneview-ansible-collection module is available in the Docker Hub built on top of Ubuntu OS with pre-built Python and Ansible Environments.

Please run the below commands to install HPE OneView collection from Docker Image.
```
    $ docker build -t oneview-ansible-collections .
    $ docker run -it --rm -v (pwd)/:/root/oneview-ansible-collections oneview-ansible-collections
```

That's it. If you would like to modify any role, simply modify role and re-run the image.

## Running the Playbooks:
To use a module from HPE OneView collection, we need to reference the full namespace, collection name, and modules name that you want to use:
```
    $ cd ~/.ansible/collections/ansible_collections/hpe/oneview
```

Run the ansible-test sanity to make sure the build passes all sanity tests. 
Refer to the below link for more information on the ansible sanity test options https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html
```
    $ ansible-test sanity
    $ cd playbooks
```

Create a sample or example oneview_server_profile.yml file to be used for running the playbook in the below playbooks directory.
Add the respective roles to the sample (or) example playbook oneview_server_profile.yml as shown below 
```
    ---
    - name: Using HPE OneView collection oneview_server_profile
       hosts: all
       collections:
         - hpe.oneview
           roles:
              - hpe.oneview.oneview_server_profile.yml
              - hpe.oneview.oneview_server_profile.yml_facts
```

Run the playbook as shown below:	  
```
    $ ansible-playbook oneview_server_profile.yml
```

## Examples provided in the HPE OneView Ansible Collection
Multiple examples are provided with the HPE OneView Ansible Collection Module covering all the HPE OneView key Resource endpoints such as Networks , LIG, EG and LE , Server Profile Template & Server Profile , Image Streamer etc.
This is to help Customers and partners for seamless migration.

Repository Path of Examples: https://github.com/HewlettPackard/oneview-ansible-collection/tree/master/roles

Let us consider a Key resource HPE OneView Server Profile that is very frequently used for Server Deployment.
oneview_server_profile example directory in the repo shared above follows the Ansible Collection file structure. 
It consists of the key files like oneview_server_profile/tasks/main.yml, oneview_server_profile/files/oneview_config.json, oneview_server_profile/defaults/main.yml, oneview_server_profile/meta/main.yml, oneview_server_profile/vars/main.yml
oneview_server_profile/tasks/main.yml consists of various tasks (ansible code) for Creating a Server Profile, Updating Server Profile and Deleting Server Profile.

OneView configuration parameters such as host name, IP Address, Password are read from oneview_server_profile/files/oneview_config.json. 
Parameter values are read from oneview_server_profile/defaults/main.yml and oneview_server_profile/vars/main.yml. Parameter values from /vars/main.yml will take precedence compared to /defaults/main.yml. 
oneview_server_profile/meta/main.yml is meant for Version information and Author information.

## Convert custom HPE OneView module playbooks to Ansible Collection [2.9] (or) Developing new playbook in the HPE OneView Ansible Collection module:
The file structure of the Ansible Collection project is different from the Ansible project.
As part of conversion of custom HPE OneView module playbooks to Ansible Collection, we would be leveraging the Task scripts from existing HPE OneView Ansible module.
Respective Task scripts from oneview-ansible/examples/ yaml files are moved to oneview-ansible-collection/roles directory.

#### Creating a collection skeleton for the Custom Playbook:
To start a custom collection:
```
    $ cd ~/.ansible/collections/ansible_collections/hpe/oneview
    $ cd roles/examples
    $ ansible-galaxy collection init oneview_custom_collection_use_case
```
Once the skeleton is created, we need to add the content to the collection. The skeleton consists of the following sub-folders 
```
    oneview_custom_collection_use_case/tasks/main.yml
    oneview_custom_collection_use_case/files/oneview_config.json
    oneview_custom_collection_use_case/defaults/main.yml
    oneview_custom_collection_use_case/meta/main.yml
    oneview_custom_collection_use_case/vars/main.yml
```

#### Adding the Content:
 * Add the ansible tasks related code in oneview_custom_collection_use_case/tasks/main.yml 
   Custom HPE OneView module Task scripts from oneview-ansible/examples/ yaml files are moved to oneview-ansible-collection/roles directory. 
   If Custom HPE OneView module has Python scripts in the oneview-ansible/library, they need to be moved to oneview-ansible-collection/plugins/ directory.
 * Add the OneView configuration such as host name, IP Address, Password to oneview_custom_collection_use_case/files/oneview_config.json 
 * Parameter values used in the tasks are read from oneview_custom_collection_use_case/defaults/main.yml and oneview_custom_collection_use_case/vars/main.yml.
   Populate the parameter values into /defaults/main.yml and /vars/main.yml based on the requirement.
 * Note that parameter values in the /vars/main.yml takes precedence when compared to /defaults/main.yml. 
 * oneview_custom_collection_use_case/meta/main.yml is meant for meta info like version, author, tags etc. Fill the version information and author details.

#### Build the Collection: To build the collection, run ansible-galaxy collection build from inside the root directory of the collection.
collection_dir#> ansible-galaxy collection build
```
    $ cd ~/.ansible/collections/ansible_collections/hpe/oneview
    $ ansible-galaxy collection build .
```
This creates a tar ball of the built collection in the current directory.
```
    $ ansible-galaxy collection install <tar_file>
```

#### Running the Playbook:
Run the ansible-test sanity to make sure the build passes all sanity tests. 
```
    $ ansible-test sanity
    $ cd playbooks
```
Create a sample or example oneview_custom_collection_use_case.yml file to be used for running the playbook in the below playbooks directory.
Add the respective roles to the sample (or) example playbook oneview_custom_collection_use_case.yml as shown below 
```
    ---
    - name: Using HPE OneView collection oneview_custom_collection_use_case
       hosts: all
       collections:
         - hpe.oneview
           roles:
              - hpe.oneview.oneview_custom_collection_use_case.yml
```
#### Run the playbook as shown below:
``` 
    $ ansible-playbook oneview_custom_collection_use_case.yml
```

## Summary:
Moving from the legacy Ansible module to the new Ansible collection, enables the user to take full advantage of infrastructure automation using Ansible Collection Modules.
The new Ansible Collection architecture streamlines and focuses Ansible development by providing an updated approach to managing the dramatically increasing volume of related content.
By migrating from the HPE OneView Ansible Module to the HPE OneView Ansible Collection, users will ensure full alignment with Ansible's development path and compatibility with Ansible products. 

This document shows that there are multiple paths to migration. That the process is straight forward and can be adjusted to suit a user's particular circumstances to achieve a seamless migration with limited effort.
GitHub, Ansible Galaxy or Automation Hub can be used to move and migrate to OneView-Ansible-collection.
Additionally, converting existing playbooks into playbooks for use with collections is a straight forward process. As is the creation of new customized playbooks for use in the new collection format.
Moving from the legacy Ansible module to the new Ansible collection requires limited effort and provides benefits which make migration a worthwhile investment.