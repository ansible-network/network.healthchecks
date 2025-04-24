from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleFilterError

DOCUMENTATION = """
    name: health_check_view
    author: Ruchi Pakhle (@Ruchip16)
    version_added: "1.0.0"
    short_description: Generate the filtered health check dict based on the provided target.
    description:
        - Generate the filtered health check dict based on the provided target.
    options:
      health_facts:
        description: Specify the health check dictionary.
        type: dict
"""

EXAMPLES = r"""
- name: health_check
  vars:
    checks:
      - name: all_neighbors_up
        ignore_errors: true
      - name: all_neighbors_down
        ignore_errors: true
      - name: min_neighbors_up
        min_count: 1
      - name: bgp_status_summary

- ansible.builtin.set_fact:
    bgp_health:
      bgp_table_version: 3
      local_as: 500
      neighbors:
        - bgp_table_version: 3
          input_queue: 0
          msg_rcvd: 52076
          msg_sent: 52111
          output_queue: 0
          peer: 12.0.0.1
          peer_as: 500
          peer_state: 1
          uptime: 4w4d
          version: 4

        - bgp_table_version: 1
          input_queue: 0
          msg_rcvd: 0
          msg_sent: 0
          output_queue: 0
          peer: "23.0.0.1"
          peer_as: 500,
          peer_state: "Idle"
          uptime: "never"
          version: 4
      path:
        memory_usage: 288
        total_entries: 2
      route_table_version: 3
      router_id: "192.168.255.229"

- name: Set health checks fact
  ansible.builtin.set_fact:
    health_checks: "{{ bgp_health | health_check_view(item) }}"
"""

RETURN = """
  health_checks:
    description: Health checks
    type: dict
"""


def health_check_view(*args, **kwargs):
    params = ["health_facts", "target"]
    data = dict(zip(params, args))
    data.update(kwargs)
    if len(data) < 2:
        raise AnsibleFilterError(
            "Missing either 'health facts' or 'target' in filter input, "
            "refer 'network.healthchecks.health_check_view' filter plugin documentation for details"
        )

    health_facts = data["health_facts"] or {}
    target = data["target"]
    health_checks = {}
    health_checks['status'] = 'PASS'

    # Handle CPU health checks
    if isinstance(target, list):
        checks = target
        data = get_health(checks)

        # CPU Health Checks
        if data['cpu_summary']:
            # Handle NX-OS CPU structure
            if 'cpu_usage' in health_facts and isinstance(health_facts['cpu_usage'], dict):
                cpu_usage = health_facts['cpu_usage']
                current_util = cpu_usage.get('five_minute', 0)
                cpu_summary = {
                    '1_min_avg': cpu_usage.get('one_minute', 0),
                    '5_min_avg': cpu_usage.get('five_minute', 0),
                    'threshold': kwargs.get('warning_threshold', 85)
                }
            # Handle IOS-XR CPU structure
            elif 'cpu' in health_facts and isinstance(health_facts['cpu'], dict):
                cpu = health_facts['cpu']
                current_util = cpu.get('5_min_avg', 0)
                cpu_summary = {
                    '1_min_avg': cpu.get('1_min_avg', 0),
                    '5_min_avg': cpu.get('5_min_avg', 0),
                    'threshold': kwargs.get('warning_threshold', 85)
                }
            # Handle IOS CPU structure
            elif 'global' in health_facts:
                cpu_summary = health_facts.get('global', {})
                current_util = cpu_summary.get('five_minute', 0)
                cpu_summary = {
                    '1_min_avg': cpu_summary.get('one_minute', 0),
                    '5_min_avg': cpu_summary.get('five_minute', 0),
                    'threshold': kwargs.get('warning_threshold', 85)
                }
            # Handle NX-OS raw CPU data
            elif 'processes' in health_facts and isinstance(health_facts['processes'], dict):
                processes = health_facts['processes']
                current_util = processes.get('five_minute', 0)
                cpu_summary = {
                    '1_min_avg': processes.get('one_minute', 0),
                    '5_min_avg': processes.get('five_minute', 0),
                    'threshold': kwargs.get('warning_threshold', 85)
                }
            else:
                current_util = 0
                cpu_summary = {
                    '1_min_avg': 0,
                    '5_min_avg': 0,
                    'threshold': kwargs.get('warning_threshold', 85)
                }

            # Set status based on thresholds
            if current_util >= kwargs.get('critical_threshold', 95):
                health_checks['status'] = 'FAIL'
            elif current_util >= kwargs.get('warning_threshold', 85):
                health_checks['status'] = 'WARNING'

            # Always include details if details flag is True
            if kwargs.get('details', False):
                health_checks['details'] = cpu_summary

        # Environment Health Checks
        if any(check['name'] in ['environment_minimum_threshold'] for check in checks):
            env_health = health_facts.get('env_health', {})
            temp_threshold = next((check.get('environment_temp_threshold', 40) for check in checks if check['name'] == 'environment_minimum_threshold'), 40)

            # Check temperature if available
            if 'temperature' in env_health:
                current_temp = env_health['temperature'].get('current_temp', 0)
                if current_temp > temp_threshold:
                    health_checks['status'] = 'FAIL'

            # Check fan status
            if 'fans' in env_health:
                fan_status = env_health['fans'].get('status', '')
                if fan_status and fan_status.lower() != 'ok':
                    health_checks['status'] = 'FAIL'

            # Check power supply if available
            if 'power' in env_health:
                power_status = env_health['power'].get('status', '')
                if power_status and power_status.lower() != 'ok':
                    health_checks['status'] = 'FAIL'

            # Always include details if details flag is True
            if kwargs.get('details', False):
                health_checks['details'] = env_health

    # Handle BGP health checks
    elif target['name'] == 'health_check':
        vars = target.get('vars', {})
        if vars:
            checks = vars.get('checks', [])
            dn_lst = []
            un_lst = []
            if health_facts.get("neighbors"):
                for item in health_facts['neighbors']:
                    # Try different possible state key names
                    state = item.get('state') or item.get('peer_state') or item.get('status')
                    if state in ('Established', 1, 'Established/OpenConfirm'):
                        item['state'] = 'Established'
                        un_lst.append(item)
                    else:
                        item['state'] = state or 'Down'
                        dn_lst.append(item)
            stats = {}
            stats['up'] = len(un_lst)
            stats['down'] = len(dn_lst)
            stats['total'] = stats['up'] + stats['down']

            details = {}
            data = get_bgp_health(checks)

            # Handle crash files health checks
            if any(check['name'] in ['crash_files', 'crash_files_summary'] for check in checks):
                crash_files = health_facts.get('crash_files', [])
                for check in checks:
                    if check['name'] == 'crash_files':
                        n_dict = {}
                        n_dict['total_crash_files'] = len(crash_files)
                        n_dict['check_status'] = 'PASS' if len(crash_files) == 0 else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'crash_files_summary':
                        n_dict = {
                            'total_crash_files': len(crash_files),
                            'crash_files': crash_files
                        }
                        health_checks[check['name']] = n_dict

            # Handle memory health checks
            if any(check['name'] in ['memory_utilization', 'memory_status_summary', 'memory_free', 'memory_buffers', 'memory_cache'] for check in checks):
                memory_stats = health_facts.get('processor_memory', {})
                for check in checks:
                    if check['name'] == 'memory_utilization':
                        n_dict = {}
                        total_mb = float(memory_stats.get('total_mb', 0))
                        used_mb = float(memory_stats.get('used_mb', 0))
                        utilization = (used_mb / total_mb * 100) if total_mb > 0 else 0
                        n_dict['current_utilization'] = round(utilization, 2)
                        n_dict['threshold'] = float(check.get('threshold', 80))
                        n_dict['check_status'] = 'PASS' if utilization <= n_dict['threshold'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'memory_status_summary':
                        n_dict = {
                            'total_mb': round(float(memory_stats.get('total_mb', 0)), 2),
                            'used_mb': round(float(memory_stats.get('used_mb', 0)), 2),
                            'free_mb': round(float(memory_stats.get('free_mb', 0)), 2)
                        }
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'memory_free':
                        n_dict = {}
                        n_dict['current_free'] = round(float(memory_stats.get('free_mb', 0)), 2)
                        n_dict['min_free'] = float(check.get('min_free', 100))
                        n_dict['check_status'] = 'PASS' if n_dict['current_free'] >= n_dict['min_free'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'memory_buffers':
                        n_dict = {}
                        n_dict['current_buffers'] = round(float(memory_stats.get('buffers_mb', 0)), 2)
                        n_dict['min_buffers'] = float(check.get('min_buffers', 50))
                        n_dict['check_status'] = 'PASS' if n_dict['current_buffers'] >= n_dict['min_buffers'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'memory_cache':
                        n_dict = {}
                        n_dict['current_cache'] = round(float(memory_stats.get('cache_mb', 0)), 2)
                        n_dict['min_cache'] = float(check.get('min_cache', 50))
                        n_dict['check_status'] = 'PASS' if n_dict['current_cache'] >= n_dict['min_cache'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict

            # Handle BGP health checks
            if data.get('summary'):
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = health_facts['neighbors']
                    n_dict['details'] = details
                health_checks[data['summary'].get('name')] = n_dict

            if data.get('all_up'):
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = health_facts['neighbors']
                    n_dict['details'] = details
                n_dict['check_status'] = 'PASS' if stats['total'] == stats['up'] else 'FAIL'
                if n_dict['check_status'] == 'FAIL' and not data['all_up'].get('ignore_errors'):
                    health_checks['status'] = 'FAIL'
                health_checks[data['all_up'].get('name')] = n_dict

            if data.get('all_down'):
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = health_facts['neighbors']
                    n_dict['details'] = details
                n_dict['check_status'] = 'PASS' if stats['total'] == stats['down'] else 'FAIL'
                if n_dict['check_status'] == 'FAIL' and not data['all_down'].get('ignore_errors'):
                    health_checks['status'] = 'FAIL'
                health_checks[data['all_down'].get('name')] = n_dict

            if data.get('min_up'):
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = health_facts['neighbors']
                    n_dict['details'] = details
                n_dict['check_status'] = 'PASS' if data['min_up']['min_count'] <= stats['up'] else 'FAIL'
                if n_dict['check_status'] == 'FAIL' and not data['min_up'].get('ignore_errors'):
                    health_checks['status'] = 'FAIL'
                health_checks[data['min_up'].get('name')] = n_dict

            # Handle interfaces health checks
            if any(check['name'] in ['all_operational_state_up', 'min_operational_state_up', 'all_admin_state_up', 'min_admin_state_up'] for check in checks):
                interfaces_stats = health_facts.get('interfaces_status_summery', {})
                for check in checks:
                    if check['name'] == 'all_operational_state_up':
                        n_dict = {}
                        n_dict.update(interfaces_stats)
                        n_dict['check_status'] = 'PASS' if interfaces_stats['total'] == interfaces_stats['up'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'min_operational_state_up':
                        n_dict = {}
                        n_dict.update(interfaces_stats)
                        n_dict['check_status'] = 'PASS' if check['min_count'] <= interfaces_stats['up'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'all_admin_state_up':
                        n_dict = {}
                        n_dict.update(interfaces_stats)
                        n_dict['check_status'] = 'PASS' if interfaces_stats['total'] == interfaces_stats['admin_up'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'min_admin_state_up':
                        n_dict = {}
                        n_dict.update(interfaces_stats)
                        n_dict['check_status'] = 'PASS' if check['min_count'] <= interfaces_stats['admin_up'] else 'FAIL'
                        if n_dict['check_status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['status'] = 'FAIL'
                        health_checks[check['name']] = n_dict

            # Update overall status
            if any(check.get('check_status') == 'FAIL' for check in health_checks.values() if isinstance(check, dict)):
                health_checks['status'] = 'FAIL'
            else:
                health_checks['status'] = 'PASS'
        else:
            health_checks = health_facts
    return health_checks


def get_bgp_status(stats, check, count=None):
    if check in ('up', 'down'):
        return 'PASS' if stats['total'] == stats[check] else 'FAIL'
    else:
        return 'PASS' if count <= stats['up'] else 'FAIL'


def get_bgp_health(checks):
    dict = {}
    dict['summary'] = is_present(checks, 'bgp_status_summary')
    dict['all_up'] = is_present(checks, 'all_neighbors_up')
    dict['all_down'] = is_present(checks, 'all_neighbors_down')
    dict['min_up'] = is_present(checks, 'min_neighbors_up')
    return dict


def get_health(checks):
    dict = {}
    dict['cpu_summary'] = is_present(checks, 'cpu_status_summary')
    return dict


def is_present(health_checks, option):
    for item in health_checks:
        if item['name'] == option:
            return get_ignore_status(item)
    return None


def get_ignore_status(item):
    if not item.get("ignore_errors"):
        item['ignore_errors'] = False
    return item


def get_interface_status(stats, check, count=None):
    if check == 'admin_up':
        return 'PASS' if stats['total'] == stats['admin_up'] else 'FAIL'
    elif check == 'oper_up':
        return 'PASS' if stats['total'] == stats['up'] else 'FAIL'
    elif check == 'min_admin':
        return 'PASS' if count <= stats['admin_up'] else 'FAIL'
    else:  # min_oper
        return 'PASS' if count <= stats['up'] else 'FAIL'


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}
