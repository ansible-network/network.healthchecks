# network.healthchecks.crashfiles

## Overview
The `network.healthchecks.crashfiles` role allows monitoring of crash files on network devices. This helps detect system crashes and stability issues, ensuring device reliability. The role provides a comprehensive health check view that shows the status of crash files and overall system health.

## Features
- Monitor presence of crash files
- Track crash file details
- Generate alerts for system crashes
- Provide detailed health check status (PASS/FAIL)
- Show crash file statistics and information

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `details` | false | no | bool | Whether to include detailed crash file information in output |

## Usage

### Example: Monitoring Crash Files
```yaml
- name: Monitor crash files
  ansible.builtin.include_role:
    name: network.healthchecks.crashfiles
  vars:
    ansible_network_os: cisco.ios.ios
    details: true
    ignore_errors: false
  register: crash_result

- name: Display crash files health check results
  ansible.builtin.debug:
    var: crash_result.health_checks
```

### Output: Crash Files Health Check Status
```json
{
    "health_checks": {
        "crash_files": {
            "status": "PASS",
            "total_crash_files": 0
        },
        "result": "PASS"
    }
}
```

### Health Check Status
- `result`: Overall health check result
  - `PASS`: No crash files found
  - `FAIL`: Crash files detected
- `crash_files`: Crash file metrics
  - `status`: Individual crash files check status
  - `total_crash_files`: Total number of crash files found

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
