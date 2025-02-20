# Ansible Network Health Checks
[![CI](https://github.com/redhat-cop/network.healthchecks/actions/workflows/tests.yml/badge.svg?event=schedule)](https://github.com/redhat-cop/network.healthchecks/actions/workflows/tests.yml)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7661/badge)](https://bestpractices.coreinfrastructure.org/projects/7661)

## About

- **Ansible Network Health Checks Collection** provides platform-agnostic roles to perform automated health checks across various network devices. 
- The collection includes capabilities for performing network device health, detecting failures, and recommending proactive maintenance.
- Designed for **network administrators, automation engineers, and IT professionals**, this collection enhances **network visibility, operational monitoring, and configuration validation**.

## Requirements
- [Requires Ansible](https://github.com/redhat-cop/network.healthchecks/blob/main/meta/runtime.yml)
- [Requires Content Collections](https://github.com/redhat-cop/network.healthchecks/blob/main/galaxy.yml)
- [Testing Requirements](https://github.com/redhat-cop/network.healthchecks/blob/main/test-requirements.txt)
- Users need to include platform-specific collections as per their requirements:
  - [arista.eos](https://github.com/ansible-collections/arista.eos)
  - [cisco.ios](https://github.com/ansible-collections/cisco.ios)
  - [cisco.iosxr](https://github.com/ansible-collections/cisco.iosxr)
  - [cisco.nxos](https://github.com/ansible-collections/cisco.nxos)
  - [junipernetworks.junos](https://github.com/ansible-collections/junipernetworks.junos)

## Installation

To consume this **Validated Content** from **Automation Hub**, add the following to your `ansible.cfg`:



## Installation
To consume this Validated Content from Automation Hub, the following needs to be added to ansible.cfg:
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

## Use Cases

`CPU Status`:
- Check CPU utilization to identify excessive resource consumption that may lead to performance degradation.
  
`Memory Status`:
- Track memory usage to detect leaks or abnormal consumption that could impact system stability. Ensure optimal memory allocation for smooth network operations.

`Environment Status`: Check environmental factors like temperature and power supply to prevent hardware failures. Detect deviations from normal conditions.

`File System Status`: Ensure sufficient disk space and check for file system errors that may affect operations. This helps to prevent storage-related failures by monitoring file system health.

`Unexpected Crash Files`: This enables users to identify unexpected core dumps and crash logs that indicate system instability. Provide early detection of software or hardware failures for faster troubleshooting.

`System Uptime`: This enables users to track system uptime to detect unexpected reboots or device restarts.

`Interfaces Status`: This enables users to run health checks on network interfaces


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