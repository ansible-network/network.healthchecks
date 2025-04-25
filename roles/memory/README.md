# network.healthchecks.memory

## Overview
The `network.healthchecks.memory` role allows monitoring of memory usage on network devices. This helps detect excessive memory consumption, ensuring device stability and performance. The role provides a comprehensive health check view that shows the status of memory utilization and overall system health.

## Features
- Monitor memory utilization with configurable thresholds
- Track available free memory
- Monitor memory buffers and cache
- Generate alerts for excessive memory usage
- Provide detailed health check status (PASS/unPASS)
- Show memory statistics (total, used, free, buffers, cache)

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `critical_threshold` | 80     | no       | int   | Memory usage percentage threshold for health check. |
| `min_free_memory` | 100    | no       | int   | Minimum free memory in MB required for health check. |
| `min_buffers` | 50     | no       | int   | Minimum buffers in MB required for health check. |
| `min_cache` | 50     | no       | int   | Minimum cache in MB required for health check. |

## Usage
### Example: Monitoring Memory Usage
```yaml
- name: Monitor memory utilization
  ansible.builtin.include_role:
    name: network.healthchecks.memory
  vars:
    ansible_network_os: cisco.ios.ios
    critical_threshold: 80
    min_free_memory: 100
    min_buffers: 50
    min_cache: 50
    ignore_errors: false
  register: memory_result

- name: Display memory health check results
  ansible.builtin.debug:
    var: memory_result.health_checks
```

### Health Check Output Example
```json
{
    "health_checks": {
        "memory_utilization": {
            "check_status": "PASS",
            "current_utilization": 45,
            "threshold": 80
        },
        "memory_free": {
            "check_status": "PASS",
            "current_free": 150,
            "min_free": 100
        },
        "memory_buffers": {
            "check_status": "PASS",
            "current_buffers": 75,
            "min_buffers": 50
        },
        "memory_cache": {
            "check_status": "PASS",
            "current_cache": 60,
            "min_cache": 50
        },
        "memory_status_summary": {
            "total_mb": 1000,
            "used_mb": 450,
            "free_mb": 550,
            "buffers_mb": 75,
            "cache_mb": 60
        },
        "status": "PASS"
    }
}
```

### Health Check Status
- `check_status`: Indicates whether each memory metric is within acceptable limits
  - `PASS`: Memory metrics are within thresholds
  - `FAIL`: Memory metrics exceed thresholds
- `status`: Overall health check status
  - `PASS`: All checks passed (or failed checks are ignored)
  - `FAIL`: At least one non-ignored check failed

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
