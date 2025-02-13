# network.healthchecks.uptime

## Overview
The `network.healthchecks.uptime` role tracks system uptime to detect unexpected reboots or device restarts.

## Features
- Monitor system uptime.
- Detect abnormal reboots.

## Usage
### Example: Checking Uptime
```yaml
- name: Monitor system uptime
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Check uptime
      ansible.builtin.include_role:
        name: network.healthchecks.uptime
## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
