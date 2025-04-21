# network.healthchecks.cpu

## Overview
The `network.healthchecks.cpu` role allows monitoring of CPU usage on network devices. This helps detect excessive CPU consumption, ensuring device stability and performance. The role provides a comprehensive health check view that shows the status of CPU utilization and overall system health.

## Features
- Monitor CPU utilization with configurable thresholds
- Detect high CPU load conditions
- Generate alerts for excessive usage
- Provide detailed health check status (successful/unsuccessful)
- Show CPU utilization statistics (5-second, 1-minute, 5-minute averages)

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `cpu_threshold` | 80     | no       | int   | CPU usage percentage threshold for health check. |

## Usage
### Example: Monitoring CPU Usage
```yaml
- name: Monitor CPU utilization
  ansible.builtin.include_role:
    name: network.healthchecks.cpu
  vars:
    ansible_network_os: cisco.ios.ios
    cpu_threshold: 80
    ignore_errors: false
  register: cpu_result

- name: Display CPU health check results
  ansible.builtin.debug:
    var: cpu_result.health_checks
```

### Health Check Output Example
```json
{
    "health_checks": {
        "cpu_utilization": {
            "check_status": "successful",
            "current_utilization": 45,
            "threshold": 80
        },
        "cpu_status_summary": {
            "five_minute": 45,
            "five_seconds": 40,
            "one_minute": 42
        },
        "status": "successful"
    }
}
```

### Health Check Status
- `check_status`: Indicates whether the CPU utilization is within acceptable limits
  - `successful`: CPU utilization is below the threshold
  - `unsuccessful`: CPU utilization exceeds the threshold
- `status`: Overall health check status
  - `successful`: All checks passed (or failed checks are ignored)
  - `unsuccessful`: At least one non-ignored check failed

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
