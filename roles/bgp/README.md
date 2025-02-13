# network.healthchecks.bgp

## Overview
The `network.healthchecks.bgp` role enables users to monitor the health and stability of BGP sessions. It ensures that BGP neighbors are up, routing tables are populated correctly.

## Features
- Validate BGP neighbor relationships.
- Detect missing or down BGP peers.
- Verify minimum neighbor thresholds.

## Variables

| Variable Name   | Default Value | Required | Type  | Description                                      |
|----------------|--------------|----------|-------|--------------------------------------------------|
| `bgp_neighbors` | `[]`         | no       | list  | List of BGP neighbors to monitor.                |
| `min_neighbors_up` | `1`       | no       | int   | Minimum number of neighbors that should be up.  |

## Usage
### Example: Checking BGP Neighbors
```yaml
- name: Check BGP neighbors
  hosts: network_devices
  gather_facts: no
  tasks:
    - name: Validate BGP status
      ansible.builtin.include_role:
        name: network.healthchecks.bgp
      vars:
        min_neighbors_up: 2
```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
