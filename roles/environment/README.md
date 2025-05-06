# network.healthchecks.environment

## Overview
The `network.healthchecks.environment` role allows monitoring of environmental conditions on network devices. This helps detect issues with temperature, fans, and power supplies, ensuring device stability and performance. The role provides a comprehensive health check view that shows the status of environmental conditions and overall system health.

## Features
- Monitor temperature with configurable thresholds
- Track fan status and speed
- Monitor power supply status
- Generate alerts for environmental issues
- Provide detailed health check status (PASS/FAIL)
- Show environmental statistics (temperature, fan status, power status)

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `environment_temp_threshold` | 40     | no       | int   | Temperature threshold in Celsius for health check. |

## Usage

### Example: Monitoring Environmental Conditions
```yaml
- name: Monitor environmental conditions
  ansible.builtin.include_role:
    name: network.healthchecks.environment
  vars:
    ansible_network_os: cisco.ios.ios
    environment_temp_threshold: 40
    ignore_errors: false
  register: env_result

- name: Display environmental health check results
  ansible.builtin.debug:
    var: env_result.health_checks
```

### Output: Environment Health Check Status
```json
{
    "health_checks": {
        "environment": {
            "status": "FAIL",
            "temperature": {
                "current_temp": 45,
                "threshold": 40
            },
            "fans": {
                "status": "NotSupported",
                "zone_speed": "Zone 1: 0x0"
            },
            "power": {
                "status": "OK"
            }
        },
        "result": "FAIL"
    }
}
```

### Health Check Status
- `result`: Overall health check status
  - `PASS`: All environmental conditions are within thresholds
  - `FAIL`: At least one environmental condition exceeds thresholds
- `environment`: Environmental metrics
  - `check_status`: Individual environment check status
  - `temperature`: Temperature metrics
    - `current_temp`: Current temperature in Celsius
    - `threshold`: Temperature threshold in Celsius
  - `fans`: Fan metrics
    - `status`: Fan status
    - `zone_speed`: Fan speed information
  - `power`: Power supply metrics
    - `status`: Power supply status

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
