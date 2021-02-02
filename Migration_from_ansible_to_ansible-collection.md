Preface:
Outline of migration to Ansible Collection:
Install and User Guide of Ansible Collection for OneView objective is to enable customers take advantage of the Infrastructure automation using Ansible Collection Modules, as well as move the current customers from the legacy Ansible module to the new Ansible collection with improved Customer experience. 

This guide covers various aspects like installation of Ansible Collection, Installation of HPE OneView Ansible Collection SDK module and running the playbooks. Provides the step by step details to the Customer for adopting / moving / migrating to oneview-ansible-collection for each of the below sections.

(a)	Installation of Ansible Collection
(b)	Installation of HPE OneView Collection SDK module
(c)	Running the Playbooks
(d)	Examples provided in the HPE OneView Collection SDK module
(e)	Conversion of existing custom Ansible Playbooks to Ansible Collection Playbooks.
(f)	Developing New Ansible Collection Playbooks.
Technical Aspects:
What aspects should I look into / check-list
1.	For leveraging HPE OneView Ansible Collection SDK module, the requirement is to have Ansible 2.10 module installed. And uninstall the Ansible module < 2.9 from the DevOps Appliance/OS if exists.
2.	Python requirements: Ansible collection works with both Python versions 2.7.9 and 3.6.x. Preferably Python 3.6.x version.
3.	The file structure of the Ansible Collection project is different from the Ansible project. Please find below the screenshot of Ansible Project structure.
 
Reusable scripts from existing HPE OneView Ansible module:
(a) Python scripts from oneview-ansible/library: Python scripts from Library module are moved to oneview-ansible-collection/plugins/ directory.
(b) Tasks scripts from oneview-ansible/examples/ yaml files are moved to oneview-ansible-collection/roles directory
We would be using ansible-galaxy executable to create the appropriate collection project structure.
ansible-galaxy collection init oneview_custom_collection_use_case 

4.	Planning: It is better for the User to plan for another DevOps appliance for running the HPE OneView Ansible Collection automation scripts.
Installation of Ansible Collection:

Requirements:
a)	As part of using the Ansible Collection in the DevOps appliance, Customer needs to uninstall the Ansible module if an installed version exists and is <= 2.9. 
b)	Download and install the Ansible 2.10 version from Red Hat portal.
c)	HPE OneView Python SDK (https://pypi.org/project/hpeOneView/)

Installation of HPE OneView Ansible Collection Modules: 
The HPE OneView collection includes roles, modules, sample playbooks, module_utils. You can install OneView Ansible Collection modules through multiple ways as listed below.

OneView Collection	GitHub	Ansible Galaxy	Automation Hub	Docker Image

Ansible OneView Collection module
	
Open Source
Community Project	Community Portal
Ansible Galaxy provides pre-packaged units of work known to Ansible as roles and collections. 
	RedHat Subscription
And Support
Ansible certified content backed by Red Hat and HPE.
	Open Source
The containerized version of the GitHub oneview-ansible-collection module is available in the Docker Store.

Install HPE OneView collection from GitHub:
https://github.com/HewlettPackard/oneview-ansible-collection
 
$ git clone https://github.com/HewlettPackard/oneview-ansible-collection.git
$ cd oneview-ansible-collection
$ ansible-galaxy collection build .
The build process will create hpe.oneview in tar file format.
$ ansible-galaxy collection install hpe.oneview

Install HPE OneView collection dependency packages:
Please run the below command to install HPE OneView collection dependency packages
$ pip install -r requirements.txt


Install HPE OneView collection from Ansible Galaxy / Red Hat Automation Hub:
Jump-start your automation project with great content from the Ansible community. Ansible Galaxy provides pre-packaged units of work known to Ansible as roles and collections. Content from roles and collections can be referenced in Ansible Playbooks and immediately put to work.
Installing collections with ansible-galaxy is only supported in Ansible version > 2.9
https://galaxy.ansible.com/hpe/oneview
 
To install HPE OneView collection hosted in Galaxy
$ ansible-galaxy collection install hpe.oneview
Please refer to below command for upgrading HPE OneView Collection to the latest version of HPE OneView:
 $ ansible-galaxy collection install hpe.oneview –force

Install HPE OneView collection dependency packages:
Please run the below command to install HPE OneView collection dependency packages
$ pip install -r requirements.txt

Install HPE OneView collection from Docker Image:
The containerized version of the oneview-ansible-collection module is available in the Docker Store built on top of Ubuntu OS with pre-built Python and Ansible Environments.
Please run the below commands to install HPE OneView collection from Docker Image.
docker build -t oneview-ansible-collections .
docker run -it --rm -v (pwd)/:/root/oneview-ansible-collections oneview-ansible-collections


That's it. If you would like to modify any role, simply modify role and re-run the image.

Running the Playbooks:

To use a module from HPE OneView collection, we need to reference the full namespace, collection name, and modules name that you want to use:

$ cd ~/.ansible/collections/ansible_collections/hpe/oneview
Run the ansible-test sanity to make sure the build passes all sanity tests. 
Refer to the below link for more information on the ansible sanity test options https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html
$ ansible-test sanity
$ cd playbooks
Add roles in sample or example.yml file to be used while running the playbook.
(hpe.oneview.oneview_fc_network)---> hpe/oneview/roles/oneview_fc_network/tasks/main.yml
---
- name: Using HPE OneView collection
   hosts: all
   collections:
     - hpe.oneview
       roles:
          - hpe.oneview.oneview_fc_network
          - hpe.oneview.oneview_fc_network_facts
$ ansible-playbook example.yml



Examples Playbooks provided with Ansible HPE OneView module
Multiple examples are provided with the HPE OneView Ansible Collection Module covering all the HPE OneView key Resource endpoints such as Networks , LIG,EG and LE , Server Profile Template & Server Profile , Image Streamer etc., . This is to help Customers and partners for seamless migration.

Repository Path of Examples: https://github.com/HewlettPackard/oneview-ansible-collection/tree/master/roles
Let us consider a Key resource HPE OneView Server Profile that is very frequently used for Server Deployment.
oneview_server_profile example directory in the repo shared above follows the Ansible Collection file structure. 
It consists of the key files like oneview_server_profile/tasks/main.yml, oneview_server_profile/files/oneview_config.json, oneview_server_profile/defaults/main.yml, oneview_server_profile/meta/main.yml, oneview_server_profile/vars/main.yml
oneview_server_profile/tasks/main.yml consists of various tasks (ansible code) for Creating a Server Profile, Updating Server Profile and Deleting Server Profile.

OneView configuration for example host name, IP Address, Password are read from oneview_server_profile/files/oneview_config.json. 
Parameter values are read from oneview_server_profile/defaults/main.yml and oneview_server_profile/vars/main.yml. Parameter values from /vars/main.yml will be taken precedence compared to /defaults/main.yml. 
oneview_server_profile/meta/main.yml is meant for Version information and Author information.

$ cd ~/.ansible/collections/ansible_collections/hpe/oneview
Run the ansible-test sanity to make sure the build passes all sanity tests. 
$ ansible-test sanity
$ cd playbooks
Create a sample or example oneview_server_profile.yml file to be used for running the playbook in the below playbooks directory.
Add the respective roles to the sample (or) example playbook oneview_server_profile.yml as shown below 
---
- name: Using HPE OneView collection oneview_server_profile
   hosts: all
   collections:
     - hpe.oneview
       roles:
          - hpe.oneview.oneview_server_profile.yml
          - hpe.oneview.oneview_server_profile.yml_facts
Run the playbook as shown below:	  
$ ansible-playbook oneview_server_profile.yml

Convert custom HPE OneView module playbooks to Ansible Collection [2.10]:

Creating a collection skeleton for the Custom Playbook:
To start a new collection:
$ cd ~/.ansible/collections/ansible_collections/hpe/oneview
$ cd roles/examples
$ ansible-galaxy collection init oneview_custom_collection_use_case
Once the skeleton is created, we need to add the content to the collection. The skeleton consists of the following sub-folders 
oneview_custom_collection_use_case/tasks/main.yml
oneview_custom_collection_use_case/files/oneview_config.json
oneview_custom_collection_use_case/defaults/main.yml
oneview_custom_collection_use_case/meta/main.yml
oneview_custom_collection_use_case/vars/main.yml

Adding the Content:
1.	Add the ansible tasks related code in oneview_custom_collection_use_case/tasks/main.yml 
2.	Add the OneView configuration such as host name, IP Address, Password to oneview_custom_collection_use_case/files/oneview_config.json 
3.	Parameter values used in the tasks are read from oneview_custom_collection_use_case/defaults/main.yml and   oneview_custom_collection_use_case/vars/main.yml. Populate the parameter values into /defaults/main.yml and /vars/main.yml based on the requirement.
4.	Note that parameter values in the /vars/main.yml takes precedence when compared to /defaults/main.yml. 
5.	oneview_custom_collection_use_case/meta/main.yml is meant for meta info like version, author, tags etc. Fill the version information and author details.

Build the Collection: To build the collection, run ansible-galaxy collection build from inside the root directory of the collection.
collection_dir#> ansible-galaxy collection build
$ cd ~/.ansible/collections/ansible_collections/hpe/oneview
$ ansible-galaxy collection build .
This creates a tar ball of the built collection in the current directory.


Running the Playbook:
Run the ansible-test sanity to make sure the build passes all sanity tests. 
$ ansible-test sanity
$ cd playbooks
Create a sample or example oneview_custom_collection_use_case.yml file to be used for running the playbook in the below playbooks directory.
Add the respective roles to the sample (or) example playbook oneview_custom_collection_use_case.yml as shown below 
---
- name: Using HPE OneView collection oneview_custom_collection_use_case
   hosts: all
   collections:
     - hpe.oneview
       roles:
          - hpe.oneview.oneview_custom_collection_use_case.yml
Run the playbook as shown below: 
$ ansible-playbook oneview_custom_collection_use_case.yml

Developing new playbook in the HPE OneView Ansible Collection module:

Creating a collection skeleton for the new playbook:
To start a new collection:
$ cd ~/.ansible/collections/ansible_collections/hpe/oneview
$ cd roles/examples
$ ansible-galaxy collection init oneview_new_collection_use_case
Once the skeleton is created, we need to add the content to the collection. The skeleton consists of the following sub-folders 
oneview_new_collection_use_case/tasks/main.yml
oneview_new_collection_use_case/files/oneview_config.json
oneview_new_collection_use_case/defaults/main.yml
oneview_new_collection_use_case/meta/main.yml
oneview_new_collection_use_case/vars/main.yml

Adding the Content:
1. Add the ansible tasks related content in oneview_new_collection_use_case/tasks/main.yml 
2. Add the OneView configuration such as host name, IP Address, Password to oneview_new_collection_use_case/files/oneview_config.json 
3. Parameter values used in the tasks are read from oneview_new_collection_use_case/defaults/main.yml and   oneview_new_collection_use_case/vars/main.yml. Populate the parameter values into /defaults/main.yml and /vars/main.yml based on the requirement.
4. Note that parameter values in the /vars/main.yml takes precedence when compared to /defaults/main.yml. 
5. oneview_new_collection_use_case/meta/main.yml is meant for meta info like version, author, tags etc. Fill the version information and author details.

Build the Collection: To build the collection, run ansible-galaxy collection build from inside the root directory of the collection.
collection_dir#> ansible-galaxy collection build
$ cd ~/.ansible/collections/ansible_collections/hpe/oneview
$ ansible-galaxy collection build .
This creates a tar ball of the built collection in the current directory.

Running the Playbook:
Run the ansible-test sanity to make sure the build passes all sanity tests. 
$ ansible-test sanity
$ cd playbooks
Create a sample or example oneview_new_collection_use_case.yml file to be used for running the playbook in the below playbooks directory.
Add the respective roles to the sample (or) example playbook oneview_new_collection_use_case.yml as shown below 
---
- name: Using HPE OneView collection oneview_new_collection_use_case
   hosts: all
   collections:
     - hpe.oneview
       roles:
          - hpe.oneview.oneview_new_collection_use_case.yml
Run the playbook as shown below: 
$ ansible-playbook oneview_new_collection_use_case.yml
