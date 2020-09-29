## dependencies_list
Manage dependencies to run resources.

#### Synopsis
 Provides an interface to manage dependencies to run resources.

#### Requirements (on the host that executes the module)
  * hpeOneView >= 5.8.0

## Example Playbook

```yaml
- hosts: all
  collections:
    - name: hpe.oneview
  roles:
    - hpe.oneview.dependencies_list
```

## License

Apache
