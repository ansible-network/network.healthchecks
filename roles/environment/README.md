# network.healthchecks.environment

## Overview
The `network.healthchecks.environment` role helps in monitoring the environmental conditions of network devices, including temperature, fan status, and power supply. This role provides a comprehensive health check view that shows the status of environmental conditions and overall system health.

## Features
- Monitor environmental temperature
- Check fan status and operation
- Monitor power supply conditions
- Provide detailed health check status (PASS/FAIL)
- Configurable temperature thresholds

## Variables
| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `details` | `false` | no | bool | Whether to include detailed environmental information in output |
| `environment_temp_threshold` | `40` | no | int | Temperature threshold in Celsius for health check |

## Usage

### Example: Checking Environment Health
```yaml
- name: Check environment health
  ansible.builtin.include_role:
    name: network.healthchecks.environment
  vars:
    details: true
    checks:
      - name: "environment minimum threshold"
        environment_temp_threshold: 40
  register: env_result

- name: Display environment health check results
  ansible.builtin.debug:
    var: env_result.health_checks
```

### Output: Environment Health Check Status
```json
{
    "ansible_facts": {
        "health_checks": {
            "status": "PASS",
            "details": {
                "fans": {
                    "air_filter": "NotSupported",
                    "zone_speed": "Zone 1: 0x0"
                }
            }
        }
    },
    "changed": false
}
```

### Health Check Status
- `status`: Overall health check status (PASS/FAIL)
  - PASS: All environmental conditions are within acceptable thresholds
  - FAIL: Any environmental condition exceeds configured thresholds
- `details`: Detailed environmental information (when details=true)
  - `fans`: Fan status information
    - `air_filter`: Air filter status
    - `zone_speed`: Fan zone speed information
  - `temperature`: Temperature readings (when available)
  - `power`: Power supply information (when available)

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
