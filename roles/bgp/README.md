# network.healthchecks.bgp

## Overview
The `network.healthchecks.bgp` role helps in monitoring BGP (Border Gateway Protocol) neighbor status and session health on network devices. This role provides a comprehensive health check view that shows the status of BGP sessions and overall routing health.

## Features
- Monitor BGP neighbor status
- Check BGP session health
- Track BGP route table version
- Provide detailed health check status (PASS/FAIL)
- Configurable neighbor checks

## Variables

| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `details` | `false` | no | bool | Whether to include detailed BGP information in output |
| `ignore_errors` | `false` | no | bool | Whether to ignore BGP neighbor down conditions |

## Usage

### Example: Checking BGP Health
```yaml
- name: Check BGP health
  ansible.builtin.include_role:
    name: network.healthchecks.bgp
  vars:
    details: true
    checks:
      - name: "all_neighbors_up"
        ignore_errors: false
      - name: "all_neighbors_down"
        ignore_errors: false
      - name: "min_neighbors_up"
        min_count: 1
  register: bgp_result

- name: Display BGP health check results
  ansible.builtin.debug:
    var: bgp_result.health_checks
```

### Output: BGP Health Check Status
```json
{
    "health_checks": {
        "all_neighbors_down": {
            "check_status": "PASS",
            "details": {
                "neighbors": [
                    {
                        "peer": "192.0.2.2",
                        "peer_as": 65002,
                        "state": "Idle",
                        "up_down": "never",
                        "version": 4
                    }
                ]
            },
            "down": 1,
            "total": 1,
            "up": 0
        },
        "all_neighbors_up": {
            "check_status": "FAIL",
            "details": {
                "neighbors": [
                    {
                        "peer": "192.0.2.2",
                        "peer_as": 65002,
                        "state": "Idle",
                        "up_down": "never",
                        "version": 4
                    }
                ]
            },
            "down": 1,
            "total": 1,
            "up": 0
        },
        "min_neighbors_up": {
            "check_status": "FAIL",
            "details": {
                "neighbors": [
                    {
                        "peer": "192.0.2.2",
                        "peer_as": 65002,
                        "state": "Idle",
                        "up_down": "never",
                        "version": 4
                    }
                ]
            },
            "down": 1,
            "total": 1,
            "up": 0
        },
        "status": "FAIL"
    }
}
```

### Health Check Status
- `status`: Overall health check status (PASS/FAIL)
  - PASS: All BGP neighbors are in Established state
  - FAIL: Any BGP neighbor is not in Established state
- `all_neighbors_up`: Check for all neighbors being up
  - `check_status`: Status of the check (PASS/FAIL)
  - `up`: Number of neighbors in Established state
  - `down`: Number of neighbors not in Established state
  - `total`: Total number of configured neighbors
  - `details`: Detailed neighbor information (when details=true)
    - `neighbors`: List of BGP neighbors with their states and statistics
- `all_neighbors_down`: Check for all neighbors being down
  - Same structure as all_neighbors_up
- `min_neighbors_up`: Check for minimum number of neighbors up
  - Same structure as all_neighbors_up
  - `min_count`: Minimum number of neighbors that should be up

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
