#!/usr/bin/env python3
"""
Network Configuration Compliance Auditor
"""

from netmiko import ConnectHandler
from .compliance_rules import ALL_CHECKS
import json
from datetime import datetime
import os

def audit_single_device(device_info):
    """
    Run all compliance checks against a single device
    """
    print(f"🔍 Auditing {device_info['host']}...")
    
    results = {
        'device': device_info['host'],
        'timestamp': datetime.now().isoformat(),
        'checks': {},
        'summary': {'passed': 0, 'failed': 0, 'total': 0}
    }
    
    try:
        # Connect to device
        connection = ConnectHandler(**device_info)
        connection.enable()
        
        # Run each compliance check
        for check in ALL_CHECKS:
            check_name = check.__name__
            result = check(connection)
            
            results['checks'][check_name] = result
            results['summary']['total'] += 1
            
            if result['passed']:
                results['summary']['passed'] += 1
            else:
                results['summary']['failed'] += 1
        
        connection.disconnect()
        print(f"✅ Completed audit for {device_info['host']}")
        
    except Exception as e:
        print(f"❌ Failed to audit {device_info['host']}: {str(e)}")
        results['error'] = str(e)
    
    return results

def calculate_compliance_score(results):
    """Calculate overall compliance percentage"""
    if results['summary']['total'] == 0:
        return 0
    
    return (results['summary']['passed'] / results['summary']['total']) * 100

def audit_multiple_devices(devices):
    """Audit multiple devices and compile results"""
    all_results = []
    
    for device in devices:
        result = audit_single_device(device)
        result['compliance_score'] = calculate_compliance_score(result)
        all_results.append(result)
    
    return all_results

def save_results(results, output_dir):
    """Save audit results to JSON file"""
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"compliance_audit_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Results saved to {filepath}")
    return filepath