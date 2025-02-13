# network.healthchecks.interfaces

## Overview
The role enables user to perform `network.interfaces` health checks.

Users would be able to perform health checks for INTERFACES resources. These health checks should be able to provide the interface's admin operational state with the necessary details.

## Features
- Detect interface errors and drops.
- Monitor bandwidth utilization.

## Usage
### Example: Checking Interface Health
```yaml
- name: Perform interface health checks
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Check interface errors and status
      ansible.builtin.include_role:
        name: network.healthchecks.interfaces
      vars:
        checks:
          - name: all_operational_state_up
          - name: min_operational_state_up
            min_count: 1
          - name: all_admin_state_up
          - name: min_admin_state_up
            min_count: 1
```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
