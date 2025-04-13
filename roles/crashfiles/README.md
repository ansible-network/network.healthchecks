# network.healthchecks.crash_files

## Overview
The `network.healthchecks.crash_files` role helps in detecting unexpected crash logs or core dumps on network devices. These logs may indicate hardware or software failures.

## Features
- Identify crash files or core dumps.

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `log_directory` | `"/var/logs/crash"` | no | str  | Directory path to check for crash files.        |

## Usage
### Example: Checking for Crash Logs
```yaml
- name: Detect crash files
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Scan for crash logs
      ansible.builtin.include_role:
        name: network.healthchecks.crash_files
```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
