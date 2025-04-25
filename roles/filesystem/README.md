# network.healthchecks.filesystem

## Overview
The `network.healthchecks.filesystem` role allows monitoring of filesystem usage on network devices. This helps detect insufficient disk space, ensuring device stability and performance. The role provides a comprehensive health check view that shows the status of filesystem utilization and overall system health.

## Features
- Monitor filesystem utilization with configurable thresholds
- Detect low disk space conditions
- Generate alerts for insufficient free space
- Provide detailed health check status (PASS/FAIL)
- Show filesystem statistics (total space, free space, utilization percentage)

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `filesystem_free_threshold` | 10     | no       | int   | Minimum free space percentage threshold for health check. |

## Usage

### Example: Monitoring Filesystem Usage
```yaml
- name: Monitor filesystem utilization
  ansible.builtin.include_role:
    name: network.healthchecks.filesystem
  vars:
    filesystem_free_threshold: 10
    ignore_errors: false
  register: fs_result

- name: Display filesystem health check results
  ansible.builtin.debug:
    var: fs_result.health_checks
```

### Output: Filesystem Health Check Status
```json
{
    "health_checks": {
        "filesystem": {
            "check_status": "PASS",
            "free_percent": 93.42,
            "threshold": 10,
            "total": 2001584128,
            "free": 1869959168
        },
        "status": "PASS"
    }
}
```

### Health Check Status
- `status`: Overall health check status
  - `PASS`: Free space is above the threshold
  - `FAIL`: Free space is below the threshold
- `filesystem`: Filesystem metrics
  - `check_status`: Individual filesystem check status
  - `free_percent`: Current free space percentage
  - `threshold`: Configured free space threshold
  - `total`: Total filesystem space in bytes
  - `free`: Free filesystem space in bytes

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
