# network.healthchecks.crash_files

## Overview
The `network.healthchecks.crash_files` role helps in detecting unexpected crash logs or core dumps on network devices. These logs may indicate hardware or software failures. The role provides a comprehensive health check view that shows the status of crash files and overall system health.

## Features
- Detect crash files or core dumps
- Generate alerts for crash file presence
- Provide detailed health check status (PASS/FAIL)
- Show crash file summary and details

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `log_directory` | `"/var/logs/crash"` | no | str  | Directory path to check for crash files.        |
| `details` | `false` | no | bool | Whether to include detailed crash file information in output |

## Usage

### Example: Checking for Crash Files
```yaml
- name: Detect crash files
  ansible.builtin.include_role:
    name: network.healthchecks.crash_files
  vars:
    details: true
  register: crash_result

- name: Display crash files health check results
  ansible.builtin.debug:
    var: crash_result.health_checks
```

### Output: Crash Files Health Check Status
```json
{
    "ansible_facts": {
        "health_checks": {
            "status": "PASS"
        }
    },
    "changed": false
}
```

### Health Check Status
- `status`: Overall health check status (PASS/FAIL)
  - PASS: No crash files detected
  - FAIL: Crash files detected

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
