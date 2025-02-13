# network.healthchecks.environment

## Overview
The `network.healthchecks.environment` role allows monitoring of environmental parameters like temperature, power supply, and fan health.

## Features
- Monitor temperature thresholds.
- Detect power supply failures.
- Check fan status.

## Usage
### Example: Checking Environmental Conditions
```yaml
- name: Monitor Environmental Conditions
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Check temperature and power supply
      ansible.builtin.include_role:
        name: network.healthchecks.environment
      vars:
        temperature_threshold: 60
```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
