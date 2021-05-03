## oneview_user
Manage OneView Users.

#### Synopsis
 Provides an interface to manage Users. Can create, update, and delete.

#### Requirements (on the host that executes the module)
  * python >= 3.4.2
  * hpeOneView >= 6.1.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| config  |   No  |  | |  Path to a .json configuration file containing the OneView client configuration. The configuration file is optional. If the file path is not provided, the configuration will be loaded from environment variables.  |
| data  |   Yes  |  | |  List with the User properties.  |
| state  |   |  | <ul> <li>present</li>  <li>absent</li> <li>set_password</li> <li>add_role_to_username</li> <li>update_role_to_username</li> <li>remove_role_from_username</li> <li>add_multiple_users</li> <li>delete_multiple_users</li> <li>validate_user_name</li> <li>validate_full_name</li> </ul> |  Indicates the desired state for the User. `present` will ensure data properties are compliant with OneView. `absent` will remove the resource from OneView, if it exists. `set_password` will changes the default administrator's password during first-time appliance setup only. `add_role_to_username` will add a given set of roles to an existing user. `update_role_to_username` will replaces a user's roles with a specified set. `remove_role_from_username` will removes a set of roles that are unrestricted by scope from a user. `add_multiple_users` will adds multiple new local users to the appliance and one must have the user create permissions. `delete_multiple_users` will removes multiple users based on query criteria. `validate_username` will validates the existence of a user with the given user name in the appliance. `validate_fullname` will checks for the existence of a user with the specified full name in the appliance. |

## Example Playbook

```yaml
- hosts: all
  collections:
    - hpe.oneview
  roles:
    - hpe.oneview.oneview_user
```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| user   | Has the facts about the OneView Users. |  Always. |  dict |
