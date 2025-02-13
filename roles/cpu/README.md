# network.healthchecks.cpu

## Overview
The `network.healthchecks.cpu` role allows monitoring of CPU usage on network devices. This helps detect excessive CPU consumption, ensuring device stability and performance.

## Features
- Monitor CPU utilization.
- Detect high CPU load conditions.
- Generate alerts for excessive usage.

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `warning_threshold` | ``     | no       | int   | CPU usage percentage to trigger a warning.       |
| `critical_threshold` | ``    | no       | int   | CPU usage percentage to trigger a critical alert.|
| `duration` | ``    | no       | int   |  The period over which the CPU usage is averaged.|

## Usage
### Example: Monitoring CPU Usage
```yaml
- name: Monitor CPU utilization
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Check CPU status
      ansible.builtin.include_role:
        name: network.healthchecks.cpu
      vars:
        warning_threshold: 80
        critical_threshold: 95
        duration: 8
```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
