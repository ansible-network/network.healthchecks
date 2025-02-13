# network.healthchecks.filesystem

## Overview
The `network.healthchecks.filesystem` role ensures that devices have sufficient disk space and identifies file system errors.

## Features
- Check available disk space.
- Detect file system corruption.

## Usage
### Example: Checking Disk Usage
```yaml
- name: Check file system status
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Verify disk space availability
      ansible.builtin.include_role:
        name: network.healthchecks.filesystem
        min_free_space: 200  # Minimum 200MB free space required

```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
