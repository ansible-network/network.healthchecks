# network.healthchecks.interfaces

## Overview
The role enables users to perform interface health checks on network devices. It provides comprehensive monitoring of interface states and operational status.

## Features
- Monitor interface operational and administrative states
- Track interface status summary including:
  - Total interfaces
  - Up/Down interfaces
  - Admin Up/Down interfaces
- Detailed interface status information including:
  - Interface name
  - Administrative state
  - Operational state

## Usage
### Example: Checking Interface Health
```yaml
- name: Perform interface health checks
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Check interface status
      ansible.builtin.include_role:
        name: network.healthchecks.interfaces
      vars:
        checks:
          - name: all_operational_state_up
          - name: min_operational_state_up
            min_count: 1
          - name: all_admin_state_up
          - name: min_admin_state_up
            min_count: 1
```

### Output Example
```json
{
    "health_checks": {
        "all_admin_state_up": {
            "check_status": "FAIL",
            "interfaces_status_summery": {
                "admin_down": 1,
                "admin_up": 5,
                "down": 1,
                "total": 6,
                "up": 5
            }
        },
        "all_operational_state_up": {
            "check_status": "FAIL",
            "interfaces_status_summery": {
                "admin_down": 1,
                "admin_up": 5,
                "down": 1,
                "total": 6,
                "up": 5
            }
        },
        "detailed_interface_status_summery": {
            "interfaces": {
                "GigabitEthernet1": {
                    "admin": "up",
                    "name": "GigabitEthernet1",
                    "operational": "up"
                },
                "GigabitEthernet2": {
                    "admin": "up",
                    "name": "GigabitEthernet2",
                    "operational": "up"
                },
                "GigabitEthernet3": {
                    "admin": "up",
                    "name": "GigabitEthernet3",
                    "operational": "up"
                },
                "GigabitEthernet4": {
                    "admin": "down",
                    "name": "GigabitEthernet4",
                    "operational": "down"
                },
                "Loopback888": {
                    "admin": "up",
                    "name": "Loopback888",
                    "operational": "up"
                },
                "Loopback999": {
                    "admin": "up",
                    "name": "Loopback999",
                    "operational": "up"
                }
            }
        },
        "min_admin_state_up": {
            "check_status": "PASS",
            "interfaces_status_summery": {
                "admin_down": 1,
                "admin_up": 5,
                "down": 1,
                "total": 6,
                "up": 5
            }
        },
        "min_operational_state_up": {
            "check_status": "PASS",
            "interfaces_status_summery": {
                "admin_down": 1,
                "admin_up": 5,
                "down": 1,
                "total": 6,
                "up": 5
            }
        },
        "status": "FAIL"
    }
}
```

## Health Check Types
- `all_operational_state_up`: Checks if all interfaces are operationally up
- `min_operational_state_up`: Checks if at least the specified minimum number of interfaces are operationally up
- `all_admin_state_up`: Checks if all interfaces are administratively up
- `min_admin_state_up`: Checks if at least the specified minimum number of interfaces are administratively up

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
