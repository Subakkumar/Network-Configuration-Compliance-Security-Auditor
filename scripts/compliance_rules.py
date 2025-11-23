"""
Define security compliance rules for network devices
Each rule returns: {passed: bool, details: str, severity: str}
"""

def check_ssh_timeout(connection):
    """Check if SSH timeout is properly configured"""
    try:
        output = connection.send_command('show run | include ssh')
        if 'time-out' in output.lower() and 'ip ssh time-out 60' in output:
            return {'passed': True, 'details': 'SSH timeout set to 60 seconds', 'severity': 'medium'}
        else:
            return {'passed': False, 'details': 'SSH timeout not properly configured', 'severity': 'medium'}
    except Exception as e:
        return {'passed': False, 'details': f'Error checking SSH: {str(e)}', 'severity': 'medium'}

def check_telnet_disabled(connection):
    """Ensure telnet is disabled"""
    try:
        output = connection.send_command('show run | include telnet')
        if 'transport input telnet' in output.lower():
            return {'passed': False, 'details': 'Telnet is enabled - security risk!', 'severity': 'high'}
        else:
            return {'passed': True, 'details': 'Telnet is disabled', 'severity': 'high'}
    except Exception as e:
        return {'passed': False, 'details': f'Error checking telnet: {str(e)}', 'severity': 'high'}

def check_aaa_configured(connection):
    """Check if AAA authentication is configured"""
    try:
        output = connection.send_command('show run | include aaa')
        if 'aaa new-model' in output:
            return {'passed': True, 'details': 'AAA authentication enabled', 'severity': 'high'}
        else:
            return {'passed': False, 'details': 'AAA authentication not configured', 'severity': 'high'}
    except Exception as e:
        return {'passed': False, 'details': f'Error checking AAA: {str(e)}', 'severity': 'high'}

def check_ntp_configured(connection):
    """Verify NTP is configured for time synchronization"""
    try:
        output = connection.send_command('show ntp status')
        if 'synchronised' in output.lower() or 'synchronized' in output.lower():
            return {'passed': True, 'details': 'NTP is synchronized', 'severity': 'medium'}
        else:
            return {'passed': False, 'details': 'NTP not synchronized', 'severity': 'medium'}
    except Exception as e:
        return {'passed': False, 'details': f'Error checking NTP: {str(e)}', 'severity': 'medium'}

def check_logging_configured(connection):
    """Check if logging to external server is configured"""
    try:
        output = connection.send_command('show run | include logging')
        if 'logging host' in output:
            return {'passed': True, 'details': 'Syslog server configured', 'severity': 'medium'}
        else:
            return {'passed': False, 'details': 'No syslog server configured', 'severity': 'medium'}
    except Exception as e:
        return {'passed': False, 'details': f'Error checking logging: {str(e)}', 'severity': 'medium'}

def check_banner_configured(connection):
    """Verify login banner is configured"""
    try:
        output = connection.send_command('show run | include banner')
        if 'banner motd' in output:
            return {'passed': True, 'details': 'Login banner configured', 'severity': 'low'}
        else:
            return {'passed': False, 'details': 'No login banner configured', 'severity': 'low'}
    except Exception as e:
        return {'passed': False, 'details': f'Error checking banner: {str(e)}', 'severity': 'low'}

def check_cdp_disabled_on_user_ports(connection):
    """Check if CDP is disabled on user-facing interfaces"""
    try:
        output = connection.send_command('show cdp interface')
        # Count CDP enabled interfaces
        lines = output.split('\n')
        enabled_count = sum(1 for line in lines if 'line protocol' in line and 'up' in line)
        
        if enabled_count > 2:  # Allow on trunk ports
            return {'passed': False, 'details': f'CDP enabled on {enabled_count} interfaces - potential security risk', 'severity': 'medium'}
        else:
            return {'passed': True, 'details': 'CDP properly configured', 'severity': 'medium'}
    except Exception as e:
        return {'passed': False, 'details': f'Error checking CDP: {str(e)}', 'severity': 'medium'}

# List of all compliance checks to run
ALL_CHECKS = [
    check_ssh_timeout,
    check_telnet_disabled,
    check_aaa_configured,
    check_ntp_configured,
    check_logging_configured,
    check_banner_configured,
    check_cdp_disabled_on_user_ports
]