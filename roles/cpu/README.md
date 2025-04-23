# network.healthchecks.cpu

## Overview
The `network.healthchecks.cpu` role allows monitoring of CPU usage on network devices. This helps detect excessive CPU consumption, ensuring device stability and performance. The role provides a comprehensive health check view that shows the status of CPU utilization and overall system health.

## Features
- Monitor CPU utilization with configurable thresholds
- Detect high CPU load conditions
- Generate alerts for excessive usage
- Provide detailed health check status (PASS/FAIL)
- Show CPU utilization statistics (1-minute, 5-minute averages)

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

### Output: CPU Health Check Status
```json
{
    "ansible_facts": {
        "health_checks": {
            "details": {
                "1_min_avg": 0,
                "5_min_avg": 0,
                "threshold": 80
            },
            "status": "PASS"
        }
    },
    "changed": false
}
```

### Health Check Status
- `status`: Overall health check status
- `details`: CPU metrics
  - `1_min_avg`: 1-minute CPU utilization average
  - `5_min_avg`: 5-minute CPU utilization average
  - `threshold`: CPU utilization threshold (default: 80)

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
