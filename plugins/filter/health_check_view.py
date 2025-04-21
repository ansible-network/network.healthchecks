from __future__ import absolute_import, division, print_function

__metaclass__ = type

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
      - name: cpu_utilization
        threshold: 80
      - name: cpu_status_summary
      - name: memory_utilization
        threshold: 80
      - name: memory_status_summary
      - name: memory_free
        min_free: 100
      - name: memory_buffers
        min_buffers: 50
      - name: memory_cache
        min_cache: 50
      - name: crash_files
        max_count: 0
      - name: environment_status
      - name: filesystem_utilization
        threshold: 80
      - name: ospf_neighbors
        min_count: 1

- ansible.builtin.set_fact:
    health_checks: "{{ health_facts | network.healthchecks.health_check_view(health_check) }}"
"""

RETURN = """
  health_checks:
    description: Health checks
    type: dict
"""

from ansible.errors import AnsibleFilterError


def health_check_view(*args, **kwargs):
    params = ["health_facts", "target"]
    data = dict(zip(params, args))
    data.update(kwargs)

    if len(data) < 2:
        raise AnsibleFilterError(
            "Missing either 'health facts' or 'target' in filter input, "
            "refer 'network.healthchecks.health_check_view' filter plugin documentation for details"
        )

    health_facts = data["health_facts"]
    target = data["target"]
    health_checks = {}
    health_checks['status'] = 'successful'

    if target['name'] == 'health_check':
        vars = target.get('vars')
        if vars:
            checks = vars.get('checks')
            data = get_health(checks)

            # CPU Health Checks
            if data['cpu_utilization']:
                check_cpu_utilization(health_facts, health_checks, data['cpu_utilization'])

            if data['cpu_summary']:
                # Handle NX-OS CPU structure
                if 'cpu_usage' in health_facts and isinstance(health_facts['cpu_usage'], dict):
                    cpu_usage = health_facts['cpu_usage']
                    cpu_summary = {
                        'five_minute': cpu_usage.get('five_minute', 0),
                        'one_minute': cpu_usage.get('one_minute', 0),
                        'five_seconds': cpu_usage.get('five_seconds', 0)
                    }
                    health_checks[data['cpu_summary'].get('name')] = cpu_summary
                # Handle IOS-XR CPU structure
                elif 'cpu' in health_facts and isinstance(health_facts['cpu'], dict):
                    cpu = health_facts['cpu']
                    cpu_summary = {
                        'five_minute': cpu.get('15_min_avg', 0),
                        'one_minute': cpu.get('1_min_avg', 0),
                        'five_seconds': cpu.get('5_min_avg', 0)
                    }
                    health_checks[data['cpu_summary'].get('name')] = cpu_summary
                # Handle IOS CPU structure
                elif 'global' in health_facts:
                    cpu_summary = health_facts.get('global', {})
                    health_checks[data['cpu_summary'].get('name')] = cpu_summary
                # Handle NX-OS raw CPU data
                elif 'processes' in health_facts and isinstance(health_facts['processes'], dict):
                    processes = health_facts['processes']
                    cpu_summary = {
                        'five_minute': processes.get('five_minute', 0),
                        'one_minute': processes.get('one_minute', 0),
                        'five_seconds': processes.get('five_seconds', 0)
                    }
                    health_checks[data['cpu_summary'].get('name')] = cpu_summary
                # Skip if no matching structure found
                else:
                    pass

            # Memory Health Checks
            if data['memory_utilization']:
                check_memory_utilization(health_facts, health_checks, data['memory_utilization'])

            if data['memory_summary']:
                memory = health_facts.get('processor_memory', {})
                # Handle IOS-XR memory structure
                if 'physical_memory' in health_facts and isinstance(health_facts['physical_memory'], dict):
                    physical_memory = health_facts['physical_memory']
                    total = physical_memory.get('total', 0)
                    available = physical_memory.get('available', 0)
                    memory_summary = {
                        'total_mb': total,
                        'used_mb': total - available,
                        'free_mb': available,
                        'largest_mb': available,
                        'lowest_mb': 0
                    }
                # Handle NX-OS and IOS memory structure
                elif 'memory_usage' in health_facts and isinstance(health_facts['memory_usage'], dict):
                    memory_usage = health_facts['memory_usage']
                    memory_summary = {
                        'total_mb': int(memory_usage.get('total', 0) / (1024 * 1024)),
                        'used_mb': int(memory_usage.get('used', 0) / (1024 * 1024)),
                        'free_mb': int(memory_usage.get('free', 0) / (1024 * 1024)),
                        'largest_mb': int(memory_usage.get('free', 0) / (1024 * 1024)),
                        'lowest_mb': 0
                    }
                # Handle IOS memory structure with MB values
                else:
                    memory_summary = {
                        'total_mb': memory.get('total_mb', 0),
                        'used_mb': memory.get('used_mb', 0),
                        'free_mb': memory.get('free_mb', 0),
                        'largest_mb': int(memory.get('largest', 0) / (1024 * 1024)) if memory.get('largest') else 0,
                        'lowest_mb': int(memory.get('lowest', 0) / (1024 * 1024)) if memory.get('lowest') else 0
                    }
                health_checks[data['memory_summary'].get('name')] = memory_summary

            if data['memory_free']:
                check_memory_free(health_facts, health_checks, data['memory_free'])

            if data['memory_buffers']:
                check_memory_buffers(health_facts, health_checks, data['memory_buffers'])

            if data['memory_cache']:
                check_memory_cache(health_facts, health_checks, data['memory_cache'])

            # Crash Files Health Check
            if data['crash_files']:
                check_crash_files(health_facts, health_checks, data['crash_files'])

            # Environment Health Check
            if data['environment']:
                health_checks[data['environment'].get('name')] = health_facts.get('environment', {})

            # Filesystem Health Checks
            if data['filesystem_utilization']:
                check_filesystem_utilization(health_facts, health_checks, data['filesystem_utilization'])
            
            if data['filesystem_summary']:
                health_checks[data['filesystem_summary'].get('name')] = health_facts.get('filesystem', {})

            # OSPF Health Checks
            if data['ospf_neighbors']:
                check_ospf_neighbors(health_facts, health_checks, data['ospf_neighbors'])
            
            if data['ospf_summary']:
                health_checks[data['ospf_summary'].get('name')] = health_facts.get('ospf', {})

            # Uptime Health Checks
            if data['uptime']:
                check_uptime(health_facts, health_checks, data['uptime'])
            
            if data['uptime_summary']:
                # Handle IOS uptime structure
                if 'uptime' in health_facts and isinstance(health_facts['uptime'], dict):
                    uptime = health_facts['uptime']
                    uptime_summary = {
                        'weeks': uptime.get('weeks', 0),
                        'days': uptime.get('days', 0),
                        'hours': uptime.get('hours', 0),
                        'minutes': uptime.get('minutes', 0)
                    }
                # Handle IOS-XR uptime structure
                elif 'uptime_parsed' in health_facts and isinstance(health_facts['uptime_parsed'], dict):
                    uptime = health_facts['uptime_parsed'].get('uptime', {})
                    uptime_summary = {
                        'weeks': uptime.get('weeks', 0),
                        'days': uptime.get('days', 0),
                        'hours': uptime.get('hours', 0),
                        'minutes': uptime.get('minutes', 0)
                    }
                # Handle NX-OS uptime structure
                elif 'system_uptime' in health_facts and isinstance(health_facts['system_uptime'], dict):
                    uptime = health_facts['system_uptime']
                    uptime_summary = {
                        'weeks': uptime.get('weeks', 0),
                        'days': uptime.get('days', 0),
                        'hours': uptime.get('hours', 0),
                        'minutes': uptime.get('minutes', 0)
                    }
                else:
                    uptime_summary = {
                        'weeks': 0,
                        'days': 0,
                        'hours': 0,
                        'minutes': 0
                    }
                health_checks[data['uptime_summary'].get('name')] = uptime_summary
        else:
            health_checks = health_facts

    return health_checks


def check_cpu_utilization(health_facts, health_checks, check):
    threshold = int(check.get('threshold', 80))
    # Handle NX-OS CPU structure
    if 'cpu_usage' in health_facts and isinstance(health_facts['cpu_usage'], dict):
        cpu_usage = health_facts['cpu_usage']
        current_util = int(cpu_usage.get('five_minute', 0))
    # Handle IOS-XR CPU structure
    elif 'cpu' in health_facts and isinstance(health_facts['cpu'], dict):
        cpu = health_facts['cpu']
        current_util = int(cpu.get('15_min_avg', 0))
    # Handle IOS CPU structure
    elif 'global' in health_facts:
        current_util = int(health_facts.get('global', {}).get('five_minute', 0))
    # Handle NX-OS raw CPU data
    elif 'processes' in health_facts and isinstance(health_facts['processes'], dict):
        processes = health_facts['processes']
        current_util = int(processes.get('five_minute', 0))
    else:
        current_util = 0
    
    check_dict = {
        'current_utilization': current_util,
        'threshold': threshold,
        'check_status': 'successful' if current_util <= threshold else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_memory_utilization(health_facts, health_checks, check):
    threshold = int(check.get('threshold', 80))
    # Handle IOS-XR memory structure
    if 'physical_memory' in health_facts and isinstance(health_facts['physical_memory'], dict):
        physical_memory = health_facts['physical_memory']
        total = physical_memory.get('total', 0)
        available = physical_memory.get('available', 0)
        used = total - available
        current_util = int((used / total) * 100) if total > 0 else 0
    # Handle NX-OS and IOS memory structure
    elif 'memory_usage' in health_facts and isinstance(health_facts['memory_usage'], dict):
        memory_usage = health_facts['memory_usage']
        total = memory_usage.get('total', 0)
        used = memory_usage.get('used', 0)
        current_util = int((used / total) * 100) if total > 0 else 0
    # Handle IOS memory structure with MB values
    else:
        memory = health_facts.get('processor_memory', {})
        total = memory.get('total_mb', 0)
        used = memory.get('used_mb', 0)
        current_util = int((used / total) * 100) if total > 0 else 0
    
    check_dict = {
        'current_utilization': current_util,
        'threshold': threshold,
        'check_status': 'successful' if current_util <= threshold else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_memory_free(health_facts, health_checks, check):
    min_free = int(check.get('min_free', 100))
    # Handle IOS-XR memory structure
    if 'physical_memory' in health_facts and isinstance(health_facts['physical_memory'], dict):
        current_free = health_facts['physical_memory'].get('available', 0)
    # Handle NX-OS and IOS memory structure
    elif 'memory_usage' in health_facts and isinstance(health_facts['memory_usage'], dict):
        current_free = int(health_facts['memory_usage'].get('free', 0) / (1024 * 1024))  # Convert bytes to MB
    # Handle IOS memory structure with MB values
    else:
        memory = health_facts.get('processor_memory', {})
        current_free = memory.get('free_mb', 0)
    
    check_dict = {
        'current_free': current_free,
        'min_free': min_free,
        'check_status': 'successful' if current_free >= min_free else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_memory_buffers(health_facts, health_checks, check):
    min_buffers = int(check.get('min_buffers', 50))
    # Handle IOS-XR memory structure
    if 'physical_memory' in health_facts and isinstance(health_facts['physical_memory'], dict):
        current_buffers = 0  # IOS-XR doesn't have buffers in the same way
    # Handle NX-OS and IOS memory structure
    elif 'memory_usage' in health_facts and isinstance(health_facts['memory_usage'], dict):
        current_buffers = 0  # NX-OS doesn't have buffers in the same way
    # Handle IOS memory structure
    else:
        memory = health_facts.get('processor_memory', {})
        current_buffers = int(memory.get('buffers', 0) / (1024 * 1024))  # Convert bytes to MB
    
    check_dict = {
        'current_buffers': current_buffers,
        'min_buffers': min_buffers,
        'check_status': 'successful' if current_buffers >= min_buffers else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_memory_cache(health_facts, health_checks, check):
    min_cache = int(check.get('min_cache', 50))
    # Handle IOS-XR memory structure
    if 'physical_memory' in health_facts and isinstance(health_facts['physical_memory'], dict):
        current_cache = 0  # IOS-XR doesn't have cache in the same way
    # Handle NX-OS and IOS memory structure
    elif 'memory_usage' in health_facts and isinstance(health_facts['memory_usage'], dict):
        current_cache = 0  # NX-OS doesn't have cache in the same way
    # Handle IOS memory structure
    else:
        memory = health_facts.get('processor_memory', {})
        current_cache = int(memory.get('cache', 0) / (1024 * 1024))  # Convert bytes to MB
    
    check_dict = {
        'current_cache': current_cache,
        'min_cache': min_cache,
        'check_status': 'successful' if current_cache >= min_cache else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_crash_files(health_facts, health_checks, check):
    max_count = int(check.get('max_count', 0))
    current_count = len(health_facts.get('crash_files', []))
    
    check_dict = {
        'current_count': current_count,
        'max_count': max_count,
        'check_status': 'successful' if current_count <= max_count else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_filesystem_utilization(health_facts, health_checks, check):
    threshold = int(check.get('threshold', 80))
    current_util = int(health_facts.get('filesystem', {}).get('used_percent', 0))
    
    check_dict = {
        'current_utilization': current_util,
        'threshold': threshold,
        'check_status': 'successful' if current_util <= threshold else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_ospf_neighbors(health_facts, health_checks, check):
    min_count = int(check.get('min_count', 1))
    neighbors = health_facts.get('ospf', {}).get('neighbors', [])
    up_count = len([n for n in neighbors if n.get('state') == 'Full'])
    
    check_dict = {
        'up_count': up_count,
        'min_count': min_count,
        'total_count': len(neighbors),
        'check_status': 'successful' if up_count >= min_count else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def check_uptime(health_facts, health_checks, check):
    min_uptime = int(check.get('min_uptime', 1440))  # Default to 24 hours in minutes
    
    # Handle IOS uptime structure
    if 'uptime' in health_facts and isinstance(health_facts['uptime'], dict):
        uptime = health_facts['uptime']
        total_minutes = (
            (uptime.get('weeks', 0) * 7 * 24 * 60) +
            (uptime.get('days', 0) * 24 * 60) +
            (uptime.get('hours', 0) * 60) +
            uptime.get('minutes', 0)
        )
    # Handle IOS-XR uptime structure
    elif 'uptime_parsed' in health_facts and isinstance(health_facts['uptime_parsed'], dict):
        uptime = health_facts['uptime_parsed'].get('uptime', {})
        total_minutes = (
            (uptime.get('weeks', 0) * 7 * 24 * 60) +
            (uptime.get('days', 0) * 24 * 60) +
            (uptime.get('hours', 0) * 60) +
            uptime.get('minutes', 0)
        )
    # Handle NX-OS uptime structure
    elif 'system_uptime' in health_facts and isinstance(health_facts['system_uptime'], dict):
        uptime = health_facts['system_uptime']
        total_minutes = (
            (uptime.get('weeks', 0) * 7 * 24 * 60) +
            (uptime.get('days', 0) * 24 * 60) +
            (uptime.get('hours', 0) * 60) +
            uptime.get('minutes', 0)
        )
    else:
        total_minutes = 0
    
    check_dict = {
        'current_uptime': total_minutes,
        'min_uptime': min_uptime,
        'check_status': 'successful' if total_minutes >= min_uptime else 'unsuccessful'
    }
    
    if check_dict['check_status'] == 'unsuccessful' and not check.get('ignore_errors'):
        health_checks['status'] = 'unsuccessful'
    
    health_checks[check.get('name')] = check_dict


def get_health(checks):
    result = {
        'cpu_utilization': None,
        'cpu_summary': None,
        'memory_utilization': None,
        'memory_summary': None,
        'memory_free': None,
        'memory_buffers': None,
        'memory_cache': None,
        'crash_files': None,
        'environment': None,
        'filesystem_utilization': None,
        'filesystem_summary': None,
        'ospf_neighbors': None,
        'ospf_summary': None,
        'uptime': None,
        'uptime_summary': None
    }
    
    for check in checks:
        if check['name'] == 'cpu_utilization':
            result['cpu_utilization'] = check
        elif check['name'] == 'cpu_status_summary':
            result['cpu_summary'] = check
        elif check['name'] == 'memory_utilization':
            result['memory_utilization'] = check
        elif check['name'] == 'memory_status_summary':
            result['memory_summary'] = check
        elif check['name'] == 'memory_free':
            result['memory_free'] = check
        elif check['name'] == 'memory_buffers':
            result['memory_buffers'] = check
        elif check['name'] == 'memory_cache':
            result['memory_cache'] = check
        elif check['name'] == 'crash_files':
            result['crash_files'] = check
        elif check['name'] == 'environment_status':
            result['environment'] = check
        elif check['name'] == 'filesystem_utilization':
            result['filesystem_utilization'] = check
        elif check['name'] == 'filesystem_status_summary':
            result['filesystem_summary'] = check
        elif check['name'] == 'ospf_neighbors':
            result['ospf_neighbors'] = check
        elif check['name'] == 'ospf_status_summary':
            result['ospf_summary'] = check
        elif check['name'] == 'uptime':
            result['uptime'] = check
        elif check['name'] == 'uptime_status_summary':
            result['uptime_summary'] = check
            
    return result


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}
