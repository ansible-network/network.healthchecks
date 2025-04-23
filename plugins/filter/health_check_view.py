from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: health_check_view
    author: Ruchi Pakhle (@)
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


def health_check_view(health_facts, checks, details=False, warning_threshold=85, critical_threshold=95):
    """
    Filter plugin to transform health facts into a standardized view.

    Args:
        health_facts (dict): Raw health facts from the device
        checks (list): List of checks to include in the view
        details (bool): Whether to include detailed information
        warning_threshold (int): Warning threshold for CPU utilization
        critical_threshold (int): Critical threshold for CPU utilization

    Returns:
        dict: Standardized health check view
    """
    view = {}
    status = "PASS"
    current_util = 0
    five_min_avg = 0

    # Get CPU utilization from health facts
    if 'cpu_status_summary' in health_facts:
        # IOS CPU structure
        cpu_summary = health_facts['cpu_status_summary']
        current_util = int(cpu_summary.get('1_min_avg', 0))
        five_min_avg = int(cpu_summary.get('5_min_avg', 0))
    elif 'cpu_utilization' in health_facts:
        # IOS-XR CPU structure
        cpu_util = health_facts['cpu_utilization']
        current_util = int(cpu_util.get('1_min_avg', 0))
        five_min_avg = int(cpu_util.get('5_min_avg', 0))
    elif 'cpu_usage' in health_facts:
        # NX-OS CPU structure
        cpu_usage = health_facts['cpu_usage']
        current_util = int(cpu_usage.get('five_minute', 0))
        five_min_avg = current_util

    # Determine status based on thresholds
    if current_util >= critical_threshold:
        status = "FAIL"
    elif current_util >= warning_threshold:
        status = "WARNING"

    # Add details if requested
    if details:
        view["details"] = {
            "1_min_avg": current_util,
            "5_min_avg": five_min_avg,
            "threshold": warning_threshold
        }

    view["status"] = status
    return view


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
        'check_status': 'PASS' if current_util <= threshold else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
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
        'check_status': 'PASS' if current_util <= threshold else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
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
        'check_status': 'PASS' if current_free >= min_free else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
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
        'check_status': 'PASS' if current_buffers >= min_buffers else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
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
        'check_status': 'PASS' if current_cache >= min_cache else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
    health_checks[check.get('name')] = check_dict


def check_crash_files(health_facts, health_checks, check):
    max_count = int(check.get('max_count', 0))
    current_count = len(health_facts.get('crash_files', []))
    
    check_dict = {
        'current_count': current_count,
        'max_count': max_count,
        'check_status': 'PASS' if current_count <= max_count else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
    health_checks[check.get('name')] = check_dict


def check_filesystem_utilization(health_facts, health_checks, check):
    threshold = int(check.get('threshold', 80))
    current_util = int(health_facts.get('filesystem', {}).get('used_percent', 0))
    
    check_dict = {
        'current_utilization': current_util,
        'threshold': threshold,
        'check_status': 'PASS' if current_util <= threshold else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
    health_checks[check.get('name')] = check_dict


def check_ospf_neighbors(health_facts, health_checks, check):
    min_count = int(check.get('min_count', 1))
    neighbors = health_facts.get('ospf', {}).get('neighbors', [])
    up_count = len([n for n in neighbors if n.get('state') == 'Full'])
    
    check_dict = {
        'up_count': up_count,
        'min_count': min_count,
        'total_count': len(neighbors),
        'check_status': 'PASS' if up_count >= min_count else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
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
        'check_status': 'PASS' if total_minutes >= min_uptime else 'unPASS'
    }
    
    if check_dict['check_status'] == 'unPASS' and not check.get('ignore_errors'):
        health_checks['status'] = 'unPASS'
    
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
