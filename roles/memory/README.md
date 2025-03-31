# network.healthchecks.memory

## Overview
The `network.healthchecks.memory` role allows tracking of memory consumption to identify leaks or excessive use that could lead to performance issues.

## Features
- Monitor available memory.
- Detect high memory consumption.

## Usage
### Example: Checking Memory Utilization
```yaml
- name: Monitor Memory Utilization
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Check memory status
      ansible.builtin.include_role:
        name: network.healthchecks.memory
      vars:
        warning_threshold: 60
        critical_threshold: 90
```
## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
