# Ansible Network Health Checks
[![CI](https://github.com/redhat-cop/network.healthchecks/actions/workflows/tests.yml/badge.svg?event=schedule)](https://github.com/redhat-cop/network.healthchecks/actions/workflows/tests.yml)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7661/badge)](https://bestpractices.coreinfrastructure.org/projects/7661)

## About

- **Ansible Network Health Checks Collection** provides platform-agnostic roles to perform automated health checks across various network devices.
- The collection includes capabilities for performing network device health, detecting failures, and recommending proactive maintenance.
- Designed for **network administrators, automation engineers, and IT professionals**, this collection enhances **network visibility, operational monitoring, and configuration validation**.

### Roles

The collection includes the following roles:

<!--start collection content-->
Name | Description
--- | ---
[network.healthchecks.bgp](roles/bgp/README.md) | Monitor BGP neighbor states and session status to ensure proper routing protocol operation.
[network.healthchecks.cpu](roles/cpu/README.md) | Monitor CPU usage to detect excessive CPU consumption and ensure device stability.
[network.healthchecks.memory](roles/memory/README.md) | Monitor memory usage to detect excessive memory consumption and ensure device stability.
[network.healthchecks.uptime](roles/uptime/README.md) | Monitor system uptime to detect system stability and identify devices needing maintenance.
[network.healthchecks.environment](roles/environment/README.md) | Monitor environmental factors like temperature and power supply to prevent hardware failures.
[network.healthchecks.filesystem](roles/filesystem/README.md) | Ensure sufficient disk space and check for file system errors that may affect operations.
[network.healthchecks.crashfiles](roles/crashfiles/README.md) | Monitor crash files to detect system crashes and stability issues.
[network.healthchecks.interfaces](roles/interfaces/README.md) | Monitor interface states and operational status to ensure proper network connectivity.
[network.healthchecks.ospf](roles/ospf/README.md) | Monitor OSPF neighbor states and session status to ensure proper routing protocol operation.
<!--end collection content-->

### BGP Health Check
The `network.healthchecks.bgp` role monitors BGP neighbor states and session status to ensure proper routing protocol operation and network connectivity.

For detailed documentation, features, and examples, see the [BGP Health Check README](roles/bgp/README.md).

### CPU Health Check
The `network.healthchecks.cpu` role monitors CPU usage on network devices to detect excessive CPU consumption and ensure device stability.

For detailed documentation, features, and examples, see the [CPU Health Check README](roles/cpu/README.md).

### Memory Health Check
The `network.healthchecks.memory` role monitors memory usage on network devices to detect excessive memory consumption and ensure device stability.

For detailed documentation, features, and examples, see the [Memory Health Check README](roles/memory/README.md).

### Uptime Health Check
The `network.healthchecks.uptime` role monitors system uptime on network devices to detect system stability and identify devices that may need maintenance.

For detailed documentation, features, and examples, see the [Uptime Health Check README](roles/uptime/README.md).

### Environment Health Check
The `network.healthchecks.environment` role monitors environmental factors like temperature and power supply to prevent hardware failures.

For detailed documentation, features, and examples, see the [Environment Health Check README](roles/environment/README.md).

### Filesystem Health Check
The `network.healthchecks.filesystem` role ensures sufficient disk space and checks for file system errors that may affect operations.

For detailed documentation, features, and examples, see the [Filesystem Health Check README](roles/filesystem/README.md).

### Crash Files Health Check
The `network.healthchecks.crashfiles` role monitors crash files on network devices to detect system crashes and stability issues.

For detailed documentation, features, and examples, see the [Crash Files Health Check README](roles/crashfiles/README.md).

### Interfaces Health Check
The `network.healthchecks.interfaces` role monitors interface states and operational status to ensure proper network connectivity and identify potential link issues.

For detailed documentation, features, and examples, see the [Interfaces Health Check README](roles/interfaces/README.md).

### OSPF Health Check
The `network.healthchecks.ospf` role monitors OSPF neighbor states and session status to ensure proper routing protocol operation and network connectivity.

For detailed documentation, features, and examples, see the [OSPF Health Check README](roles/ospf/README.md).

## Health Check Status Formats

Each role provides a standardized health check output format. Here's a summary of the status formats for each role:

### BGP Health Check Status
Monitors BGP neighbor states and session status, checking for minimum required up neighbors and overall BGP health.

```json
{
    "health_checks": {
        "all_neighbors_down": {
            "status": "FAIL",
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
            "status": "PASS",
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
            "status": "PASS",
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
        "result": "PASS"
    }
}
```

### CPU Health Check Status
Tracks CPU utilization with 1-minute and 5-minute averages against a configurable threshold.

```json
{
    "health_checks": {
        "cpu_utilization": {
            "status": "PASS",
            "1_min_avg": 0,
            "5_min_avg": 0,
            "threshold": 80
        },
        "result": "PASS"
    }
}
```

### Memory Health Check Status
Monitors memory utilization percentage against a configurable threshold to prevent memory exhaustion.

```json
{
    "health_checks": {
        "memory_utilization": {
            "status": "PASS",
            "current_utilization": 45,
            "threshold": 80
        },
        "memory_free": {
            "status": "PASS",
            "current_free": 150,
            "min_free": 100,
            "free_mb": 550,
        },
        "memory_buffers": {
            "status": "PASS",
            "current_buffers": 75,
            "min_buffers": 50,
            "buffers_mb": 75,
        },
        "memory_cache": {
            "status": "PASS",
            "current_cache": 60,
            "min_cache": 50,
            "cache_mb": 60
        },
        "result": "PASS"
    }
}
```

### Uptime Health Check Status
Tracks system uptime duration and compares it against a minimum required uptime threshold.

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

### Environment Health Check Status
Monitors environmental conditions including temperature, fan status, and power supply health.

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

### Filesystem Health Check Status
Tracks filesystem usage, free space percentage, and compares against a configurable threshold.

```json
{
    "health_checks": {
        "filesystem": {
            "status": "PASS",
            "free_percent": 93.42,
            "threshold": 10,
            "total_kb": 2001584128,
            "free_kb": 1869959168
        },
        "result": "PASS"
    }
}
```

### Crash Files Health Check Status
Monitors for the presence of crash files and provides a summary of any detected system crashes.

```json
{
    "health_checks": {
        "crash_files": {
            "status": "PASS",
            "total_crash_files": 0
        },
        "result": "PASS"
    }
}
```

### Interfaces Health Check Status
Monitors interface states (administrative and operational) and provides detailed interface status information.

```json
{
    "health_checks": {
        "all_admin_state_up": {
            "status": "FAIL",
            "interfaces_status_summery": {
                "admin_down": 1,
                "admin_up": 5,
                "down": 1,
                "total": 6,
                "up": 5
            }
        },
        "all_operational_state_up": {
            "status": "FAIL",
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
        "result": "FAIL"
    }
}
```

### OSPF Health Check Status
Monitors OSPF neighbor states and session status, checking for minimum required up neighbors and overall OSPF health.

```json
{
    "ansible_facts": {
        "health_checks": {
            "all_neighbors_down": {
                "status": "FAIL",
                "details": {
                    "neighbors": [
                        {
                            "address": "10.1.1.2",
                            "area": "0.0.0.0",
                            "interface": "GigabitEthernet1",
                            "state": "FULL/BDR"
                        }
                    ]
                },
                "down": 0,
                "total": 1,
                "up": 1
            },
            "all_neighbors_up": {
                "status": "PASS",
                "details": {
                    "neighbors": [
                        {
                            "address": "10.1.1.2",
                            "area": "0.0.0.0",
                            "interface": "GigabitEthernet1",
                            "state": "FULL/BDR"
                        }
                    ]
                },
                "down": 0,
                "total": 1,
                "up": 1
            },
            "min_neighbors_up": {
                "status": "PASS",
                "details": {
                    "neighbors": [
                        {
                            "address": "10.1.1.2",
                            "area": "0.0.0.0",
                            "interface": "GigabitEthernet1",
                            "state": "FULL/BDR"
                        }
                    ]
                },
                "down": 0,
                "total": 1,
                "up": 1
            },
            "result": "PASS"
        }
    },
}
```

## Requirements
- [Requires Ansible](https://github.com/redhat-cop/network.healthchecks/blob/main/meta/runtime.yml)
- [Requires Content Collections](https://github.com/redhat-cop/network.healthchecks/blob/main/galaxy.yml)
- [Testing Requirements](https://github.com/redhat-cop/network.healthchecks/blob/main/test-requirements.txt)
- Users need to include platform-specific collections as per their requirements:
  - [arista.eos](https://github.com/ansible-collections/arista.eos)
  - [cisco.ios](https://github.com/ansible-collections/cisco.ios)
  - [cisco.iosxr](https://github.com/ansible-collections/cisco.iosxr)
  - [cisco.nxos](https://github.com/ansible-collections/cisco.nxos)

## Installation

To consume this **Validated Content** from **Automation Hub**, add the following to your `ansible.cfg`:

```
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://console.redhat.com/api/automation-hub/content/validated/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```

Utilize the current Token, and if the token has expired, obtain the necessary
token from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

With this configured, simply run the following commands:

```
ansible-galaxy collection install network.healthchecks
ansible-galaxy collection install network.bgp
```

## Testing

The project uses tox to run `ansible-lint` and `ansible-test sanity`.
Assuming this repository is checked out in the proper structure,
e.g. `collections_root/ansible_collections/network/bgp`, run:

```shell
  tox -e ansible-lint
  tox -e py39-sanity
```

To run integration tests, ensure that your inventory has a `network_bgp` group.
Depending on what test target you are running, comment out the host(s).

```shell
[network_hosts]
ios
junos

[ios:vars]
< enter inventory details for this group >

[junos:vars]
< enter inventory details for this group >
```

```shell
  ansible-test network-integration -i /path/to/inventory --python 3.9 [target]
```

## Contributing

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against this repository.

Don't know how to start? Refer to the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html)!

Want to submit code changes? Take a look at the [Quick-start development guide](https://docs.ansible.com/ansible/devel/community/create_pr_quick_start.html).

We also use the following guidelines:

* [Collection review checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_reviewing.html)
* [Ansible development guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible collection development guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

Release notes are available [here](https://github.com/redhat-cop/network.bgp/blob/main/CHANGELOG.rst).

## Related information

- [Developing network resource modules](https://github.com/ansible-network/networking-docs/blob/main/rm_dev_guide.md)
- [Ansible Networking docs](https://github.com/ansible-network/networking-docs)
- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible Roles overview](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_reuse_roles.html)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.