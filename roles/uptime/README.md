# network.healthchecks.uptime

## Overview
The `network.healthchecks.uptime` role allows monitoring of system uptime on network devices. This helps detect system stability and identify devices that may need maintenance or have experienced recent restarts. The role provides a comprehensive health check view that shows the status of system uptime and overall system health.

## Features
- Monitor system uptime with configurable thresholds
- Track uptime in weeks, days, hours, and minutes
- Generate alerts for devices with low uptime
- Provide detailed health check status (PASS/FAIL)
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
            "status": "PASS",
            "current_uptime": 5760,
            "min_uptime": 1440
        },
        "uptime_status_summary": {
            "weeks": 3,
            "days": 3,
            "hours": 22,
            "minutes": 36
        },
        "result": "PASS"
    }
}
```

### Health Check Status
- `status`: Indicates whether the system uptime meets the minimum threshold
  - `PASS`: System uptime meets or exceeds the threshold
  - `FAIL`: System uptime is below the threshold
- `result`: Overall health check status
  - `PASS`: All checks passed (or failed checks are ignored)
  - `FAIL`: At least one non-ignored check failed

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
