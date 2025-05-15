from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: filesystem_health_check_view
    author: Ruchi Pakhle (@Ruchip16)
    version_added: "1.0.0"
    short_description: Generate the filtered filesystem health check dict based on the provided target.
    description:
        - Generate the filtered filesystem health check dict based on the provided target.
    options:
      health_facts:
        description: Specify the health check dictionary.
        type: dict
"""

EXAMPLES = r"""
- name: Perform filesystem health checks
  hosts: iosxr
  gather_facts: false
  tasks:
    - name: Filesystem Manager
      ansible.builtin.include_role:
        name: network.healthchecks.filesystem
      vars:
        min_free_space_mb: 10
"""

RETURN = """
  health_checks:
    description: Filesystem health checks
    type: dict
"""

from ansible.errors import AnsibleFilterError


def _process_health_facts(health_facts):
    """Process filesystem health facts to generate summary statistics"""
    if not health_facts or 'fs_health' not in health_facts:
        return None

    fs_data = health_facts['fs_health']
    if not fs_data or 'free' not in fs_data or 'total' not in fs_data:
        return None

    return {
        'free': fs_data['free'],
        'total': fs_data['total'],
        'free_percent': round((fs_data['free'] / fs_data['total']) * 100, 2)
    }


def filesystem_health_check_view(*args, **kwargs):
    params = ["health_facts", "target"]
    data = dict(zip(params, args))
    data.update(kwargs)

    if len(data) < 2:
        raise AnsibleFilterError(
            "Missing either 'health facts' or 'target' in filter input, "
            "refer 'network.healthchecks.filesystem_health_check_view' filter plugin documentation for details"
        )

    health_facts = data["health_facts"]
    target = data["target"]

    health_checks = {}
    health_checks['result'] = 'PASS'

    if target["name"] == "health_check":
        h_vars = target.get("vars", {})
        if h_vars:
            checks = h_vars.get("checks", [])
            details = h_vars.get("details", False)

            for check in checks:
                if check['name'] == 'filesystem_status_summary':
                    fs_data = _process_health_facts(health_facts)
                    if not fs_data:
                        health_checks['result'] = 'FAIL'
                        health_checks['filesystem'] = {
                            'status': 'FAIL',
                            'error': 'Invalid filesystem data'
                        }
                        continue

                    threshold = check.get('filesystem_free_threshold', 10)
                    if fs_data['free_percent'] < threshold:
                        health_checks['result'] = 'FAIL'
                        health_checks['filesystem'] = {
                            'status': 'FAIL',
                            'free_percent': fs_data['free_percent'],
                            'threshold': threshold,
                            'total': fs_data['total'],
                            'free': fs_data['free']
                        }
                    else:
                        health_checks['filesystem'] = {
                            'status': 'PASS',
                            'free_percent': fs_data['free_percent'],
                            'threshold': threshold,
                            'total': fs_data['total'],
                            'free': fs_data['free']
                        }

                    if details:
                        health_checks['details'] = health_facts
        else:
            health_checks = health_facts

    return health_checks

class FilterModule(object):
    """filesystem_health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"filesystem_health_check_view": filesystem_health_check_view} 