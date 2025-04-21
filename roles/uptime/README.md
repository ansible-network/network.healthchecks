# network.healthchecks.uptime

## Overview
The `network.healthchecks.uptime` role allows monitoring of system uptime on network devices. This helps detect system stability and identify devices that may need maintenance or have experienced recent restarts. The role provides a comprehensive health check view that shows the status of system uptime and overall system health.

## Features
- Monitor system uptime with configurable thresholds
- Track uptime in weeks, days, hours, and minutes
- Generate alerts for devices with low uptime
- Provide detailed health check status (successful/unsuccessful)
- Show uptime statistics in human-readable format

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `uptime_threshold_minutes` | 1440 | no       | int   | Minimum uptime in minutes required for health check (default 24 hours). |

## Usage
### Example: Monitoring System Uptime
```yaml
- name: Monitor system uptime
  ansible.builtin.include_role:
    name: network.healthchecks.uptime
  vars:
    uptime_threshold_minutes: 1440  # 24 hours
  register: uptime_result

- name: Display uptime health check results
  ansible.builtin.debug:
    var: uptime_result.health_checks
```

### Health Check Output Example
```json
{
    "health_checks": {
        "uptime": {
            "check_status": "successful",
            "current_uptime": 5760,
            "min_uptime": 1440
        },
        "uptime_status_summary": {
            "weeks": 3,
            "days": 3,
            "hours": 22,
            "minutes": 36
        },
        "status": "successful"
    }
}
```

### Health Check Status
- `check_status`: Indicates whether the system uptime meets the minimum threshold
  - `successful`: System uptime meets or exceeds the threshold
  - `unsuccessful`: System uptime is below the threshold
- `status`: Overall health check status
  - `successful`: All checks passed (or failed checks are ignored)
  - `unsuccessful`: At least one non-ignored check failed

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
