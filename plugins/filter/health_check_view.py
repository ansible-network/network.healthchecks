from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import yaml
from ansible.errors import AnsibleFilterError

# Load default values from defaults/main.yml
DEFAULTS_FILE = os.path.join(os.path.dirname(__file__), 'defaults', 'main.yml')
with open(DEFAULTS_FILE, 'r') as f:
    DEFAULT_VALUES = yaml.safe_load(f)

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
    # Use passed thresholds or fall back to defaults
    threshold = int(kwargs.get('warning_threshold', health_facts.get('cpu_warning_threshold', DEFAULT_VALUES.get('cpu_warning_threshold'))))
    critical_threshold = int(kwargs.get('critical_threshold', health_facts.get('cpu_critical_threshold', DEFAULT_VALUES.get('cpu_critical_threshold'))))

    target = data["target"]
    health_checks = {}
    health_checks['result'] = 'PASS'

    # Handle CPU health checks
    if isinstance(target, list):
        checks = target
        data = get_health(checks)

        # Filesystem Health Checks
        if 'fs_health' in health_facts:
            # Handle nested fs_health structure
            fs_data = health_facts['fs_health'].get('fs_health', {})
            free_percent = (fs_data.get('free') / fs_data.get('total')) * 100
            free_threshold = kwargs.get('filesystem_free_threshold', health_facts.get('filesystem_free_threshold'))

            if not free_threshold:
                raise AnsibleFilterError(
                    "Missing required filesystem_free_threshold value. Please provide it in the playbook or defaults."
                )

            if free_percent < free_threshold:
                health_checks['result'] = 'FAIL'
                health_checks['filesystem'] = {
                    'status': 'FAIL',
                    'free_percent': round(free_percent, 2),
                    'threshold': free_threshold,
                    'total': fs_data.get('total', 0),
                    'free': fs_data.get('free', 0)
                }
            else:
                health_checks['filesystem'] = {
                    'status': 'PASS',
                    'free_percent': round(free_percent, 2),
                    'threshold': free_threshold,
                    'total': fs_data.get('total', 0),
                    'free': fs_data.get('free', 0)
                }

            # Always include details if details flag is True
            if kwargs.get('details', False):
                health_checks['details'] = fs_data

        # CPU Health Checks
        if data['cpu_utilization']:
            # Handle NX-OS CPU structure
            if 'cpu_usage' in health_facts and isinstance(health_facts['cpu_usage'], dict):
                cpu_usage = health_facts['cpu_usage']
                current_util = int(cpu_usage.get('five_minute', 0))

            # Handle IOS-XR CPU structure
            elif 'cpu' in health_facts and isinstance(health_facts['cpu'], dict):
                cpu = health_facts['cpu']
                current_util = int(cpu.get('5_min_avg', 0))

            # Handle IOS CPU structure
            elif 'global' in health_facts:
                cpu_summary = health_facts.get('global', {})
                current_util = int(cpu_summary.get('five_minute', 0))

            # Handle NX-OS raw CPU data
            elif 'processes' in health_facts and isinstance(health_facts['processes'], dict):
                processes = health_facts['processes']
                current_util = int(processes.get('five_minute', 0))

            else:
                current_util = 0

            # Set status based on threshold comparison
            if current_util >= critical_threshold:
                health_checks['result'] = 'FAIL'
                status = 'FAIL'
                message = "CPU utilization is above the critical threshold"
            elif current_util >= threshold:
                health_checks['result'] = 'WARNING'
                status = 'WARNING'
                message = "CPU utilization is above the threshold"
            else:
                status = 'PASS'
                message = "CPU utilization is within acceptable limits"

            # Add CPU utilization to health checks with exact README format
            health_checks['cpu_utilization'] = {
                'status': status,
                'message': message,
                '1_min_avg': current_util,
                '5_min_avg': current_util,
                'threshold': threshold
            }

            # Always include details if details flag is True
            if kwargs.get('details', False):
                health_checks['details'] = {
                    'cpu_utilization': {
                        'status': status,
                        'message': message,
                        '1_min_avg': current_util,
                        '5_min_avg': current_util,
                        'threshold': threshold
                    }
                }

        # Environment Health Checks
        if any(check['name'] in ['environment_minimum_threshold'] for check in checks):
            env_health = health_facts.get('env_health', {})
            temp_threshold = next(
                (check.get('environment_temp_threshold', health_facts.get('environment_temp_threshold'))
                 for check in checks if check['name'] == 'environment_minimum_threshold'),
                health_facts.get('environment_temp_threshold')
            )
            if not temp_threshold:
                raise AnsibleFilterError(
                    "Missing required environment_temp_threshold value. Please provide it in the playbook or defaults."
                )

            n_dict = {
                'status': 'PASS',
                'temperature': {
                    'current_temp': 0,
                    'threshold': float(temp_threshold)
                },
                'fans': {
                    'status': 'NotSupported',
                    'zone_speed': 'NotSupported'
                },
                'power': {
                    'status': 'NotSupported'
                }
            }

            # Check temperature if available
            if 'temperature' in env_health:
                current_temp = float(env_health['temperature'].get('current_temp', 0))
                n_dict['temperature']['current_temp'] = current_temp
                if current_temp > temp_threshold:
                    n_dict['status'] = 'FAIL'
                    health_checks['result'] = 'FAIL'

            # Check fan status
            if 'fans' in env_health:
                fan_data = env_health['fans']
                n_dict['fans'] = {
                    'status': fan_data.get('status', 'NotSupported'),
                    'zone_speed': fan_data.get('zone_speed', 'NotSupported')
                }
                if n_dict['fans']['status'] != 'OK':
                    n_dict['status'] = 'FAIL'
                    health_checks['result'] = 'FAIL'

            # Check power supply if available
            if 'power' in env_health:
                power_data = env_health['power']
                n_dict['power'] = {
                    'status': power_data.get('status', 'NotSupported')
                }
                if n_dict['power']['status'] != 'OK':
                    n_dict['status'] = 'FAIL'
                    health_checks['result'] = 'FAIL'

            # Always include the environment section in the output
            health_checks['environment'] = n_dict
            # Set overall result based on environment status
            if n_dict['status'] == 'FAIL':
                health_checks['result'] = 'FAIL'
            else:
                health_checks['result'] = 'PASS'

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
                crash_data = health_facts.get('crash_health', {})
                crash_files = crash_data.get('crash_files', [])

                for check in checks:
                    if check['name'] == 'crash_files':
                        n_dict = {
                            'status': 'PASS',
                            'total_crash_files': len(crash_files)
                        }
                        if len(crash_files) > 0:
                            n_dict['status'] = 'FAIL'
                            health_checks['result'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'crash_files_summary':
                        n_dict = {
                            'total_crash_files': len(crash_files),
                            'crash_files': crash_files
                        }
                        health_checks[check['name']] = n_dict

            # Handle memory health checks
            if any(check['name'] in ['memory_utilization', 'memory_free', 'memory_buffers', 'memory_cache'] for check in checks):
                memory_stats = health_facts.get('memory_health', {})
                for check in checks:
                    if check['name'] == 'memory_utilization':
                        n_dict = {}
                        # Handle IOS XR format
                        if 'physical_memory' in memory_stats:
                            total_mb = float(memory_stats['physical_memory'].get('total_mb', 0))
                            available_mb = float(memory_stats['physical_memory'].get('available', 0))
                            used_mb = total_mb - available_mb
                        else:
                            total_mb = float(memory_stats.get('total_mb', 0))
                            used_mb = float(memory_stats.get('used_mb', 0))

                        utilization = (used_mb / total_mb * 100) if total_mb > 0 else 0
                        n_dict['current_utilization'] = round(utilization, 2)
                        threshold = check.get('threshold', health_facts.get('memory_utilization_threshold'))
                        if not threshold:
                            raise AnsibleFilterError(
                                "Missing required memory utilization threshold. Please provide it in the playbook or defaults."
                            )
                        n_dict['threshold'] = float(threshold)
                        n_dict['status'] = 'PASS' if utilization <= n_dict['threshold'] else 'FAIL'
                        if n_dict['status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['result'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'memory_free':
                        n_dict = {}
                        # Handle IOS XR format
                        if 'physical_memory' in memory_stats:
                            n_dict['current_free'] = round(float(memory_stats['physical_memory'].get('available', 0)), 2)
                        else:
                            n_dict['current_free'] = round(float(memory_stats.get('free_mb', 0)), 2)

                        min_free = check.get('min_free', health_facts.get('memory_min_free'))
                        if not min_free:
                            raise AnsibleFilterError(
                                "Missing required min_free value for memory_free check. Please provide it in the playbook or defaults."
                            )
                        n_dict['min_free'] = float(min_free)
                        n_dict['status'] = 'PASS' if n_dict['current_free'] >= n_dict['min_free'] else 'FAIL'
                        if n_dict['status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['result'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'memory_buffers':
                        n_dict = {}
                        n_dict['current_buffers'] = round(float(memory_stats.get('buffers_mb', 0)), 2)
                        min_buffers = check.get('min_buffers', health_facts.get('memory_min_buffers'))
                        if not min_buffers:
                            raise AnsibleFilterError(
                                "Missing required min_buffers value for memory_buffers check. Please provide it in the playbook or defaults."
                            )
                        n_dict['min_buffers'] = float(min_buffers)
                        n_dict['status'] = 'PASS' if n_dict['current_buffers'] >= n_dict['min_buffers'] else 'FAIL'
                        if n_dict['status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['result'] = 'FAIL'
                        health_checks[check['name']] = n_dict
                    elif check['name'] == 'memory_cache':
                        n_dict = {}
                        n_dict['current_cache'] = round(float(memory_stats.get('cache_mb', 0)), 2)
                        min_cache = check.get('min_cache', health_facts.get('memory_min_cache'))
                        if not min_cache:
                            raise AnsibleFilterError(
                                "Missing required min_cache value for memory_cache check. Please provide it in the playbook or defaults."
                            )
                        n_dict['min_cache'] = float(min_cache)
                        n_dict['status'] = 'PASS' if n_dict['current_cache'] >= n_dict['min_cache'] else 'FAIL'
                        if n_dict['status'] == 'FAIL' and not check.get('ignore_errors'):
                            health_checks['result'] = 'FAIL'
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
                n_dict['status'] = 'PASS' if stats['total'] == stats['up'] else 'FAIL'
                if n_dict['status'] == 'FAIL' and not data['all_up'].get('ignore_errors'):
                    health_checks['result'] = 'FAIL'
                health_checks[data['all_up'].get('name')] = n_dict

            if data.get('all_down'):
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = health_facts['neighbors']
                    n_dict['details'] = details
                n_dict['status'] = 'PASS' if stats['total'] == stats['down'] else 'FAIL'
                if n_dict['status'] == 'FAIL' and not data['all_down'].get('ignore_errors'):
                    health_checks['result'] = 'FAIL'
                health_checks[data['all_down'].get('name')] = n_dict

            if data.get('min_up'):
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = health_facts['neighbors']
                    n_dict['details'] = details
                n_dict['status'] = 'PASS' if data['min_up']['min_count'] <= stats['up'] else 'FAIL'
                if n_dict['status'] == 'FAIL' and not data['min_up'].get('ignore_errors'):
                    health_checks['result'] = 'FAIL'
                health_checks[data['min_up'].get('name')] = n_dict

            # Update overall status
            if any(check.get('status') == 'FAIL' for check in health_checks.values() if isinstance(check, dict)):
                health_checks['result'] = 'FAIL'

            # Set overall result if not already set
            if 'result' not in health_checks:
                health_checks['result'] = 'PASS' if len(crash_files) == 0 else 'FAIL'
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
    dict['cpu_utilization'] = is_present(checks, 'cpu_utilization')
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


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}
