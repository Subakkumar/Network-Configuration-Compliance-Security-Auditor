#!/usr/bin/env python3
"""
Main script to run the network compliance audit - DEMO VERSION
"""

from scripts.auditor import audit_multiple_devices, save_results
from scripts.report_generator import generate_compliance_report
import os
from datetime import datetime
import json
import subprocess

def create_demo_data():
    """Create demo audit results for testing without real devices"""
    print("🔧 Creating demo data for testing...")
    
    demo_results = [
        {
            'device': 'Core-Switch-1',
            'timestamp': datetime.now().isoformat(),
            'compliance_score': 85.7,
            'summary': {'passed': 6, 'failed': 1, 'total': 7},
            'checks': {
                'check_ssh_timeout': {'passed': True, 'details': 'SSH timeout set to 60 seconds', 'severity': 'medium'},
                'check_telnet_disabled': {'passed': True, 'details': 'Telnet is disabled', 'severity': 'high'},
                'check_aaa_configured': {'passed': True, 'details': 'AAA authentication enabled', 'severity': 'high'},
                'check_ntp_configured': {'passed': True, 'details': 'NTP is synchronized', 'severity': 'medium'},
                'check_logging_configured': {'passed': False, 'details': 'No syslog server configured', 'severity': 'medium'},
                'check_banner_configured': {'passed': True, 'details': 'Login banner configured', 'severity': 'low'},
                'check_cdp_disabled_on_user_ports': {'passed': True, 'details': 'CDP properly configured', 'severity': 'medium'}
            }
        },
        {
            'device': 'Access-Switch-2', 
            'timestamp': datetime.now().isoformat(),
            'compliance_score': 42.9,
            'summary': {'passed': 3, 'failed': 4, 'total': 7},
            'checks': {
                'check_ssh_timeout': {'passed': False, 'details': 'SSH timeout not properly configured', 'severity': 'medium'},
                'check_telnet_disabled': {'passed': False, 'details': 'Telnet is enabled - security risk!', 'severity': 'high'},
                'check_aaa_configured': {'passed': False, 'details': 'AAA authentication not configured', 'severity': 'high'},
                'check_ntp_configured': {'passed': True, 'details': 'NTP is synchronized', 'severity': 'medium'},
                'check_logging_configured': {'passed': False, 'details': 'No syslog server configured', 'severity': 'medium'},
                'check_banner_configured': {'passed': True, 'details': 'Login banner configured', 'severity': 'low'},
                'check_cdp_disabled_on_user_ports': {'passed': True, 'details': 'CDP properly configured', 'severity': 'medium'}
            }
        }
    ]
    
    return demo_results

def open_file_in_browser(file_path):
    """Open the HTML file in the default web browser"""
    try:
        # Convert to absolute path
        abs_path = os.path.abspath(file_path)
        
        # Check if file exists
        if not os.path.exists(abs_path):
            print(f"❌ File not found: {abs_path}")
            return False
            
        print(f"📁 File location: {abs_path}")
        
        # Try different methods to open the file
        try:
            # Method 1: Use os.startfile (Windows)
            os.startfile(abs_path)
            print("✅ Opened report in browser!")
            return True
        except:
            # Method 2: Use subprocess
            subprocess.Popen(['start', abs_path], shell=True)
            print("✅ Opened report in browser!")
            return True
            
    except Exception as e:
        print(f"❌ Could not open file automatically: {e}")
        print(f"💡 Please manually open this file: {file_path}")
        return False

def main():
    print("🛡️ Starting Network Compliance Auditor...")
    
    # Ask user if they want demo mode or real audit
    choice = input("Choose mode: [1] Demo (no devices needed) [2] Real Audit: ")
    
    if choice == "1":
        # Use demo data
        results = create_demo_data()
        print("✅ Using demo data - no real devices required!")
    else:
        # Real device audit
        devices = [
            {
                'device_type': 'cisco_ios',
                'host': input("Enter device IP: "),  # You'll be prompted for IP
                'username': input("Enter username: "),
                'password': input("Enter password: "),
                'secret': input("Enter enable secret: "),
            }
        ]
        
        # Run audit on real devices
        results = audit_multiple_devices(devices)
    
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    # Save raw results
    results_file = save_results(results, 'outputs')
    
    # Generate HTML report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"outputs/compliance_report_{timestamp}.html"
    
    try:
        report_path = generate_compliance_report(results, 'templates/compliance_report.html', report_file)
        
        # Print summary
        if results:
            total_score = sum(r['compliance_score'] for r in results) / len(results)
            print(f"\n🎉 AUDIT COMPLETE!")
            print(f"   📊 Devices Audited: {len(results)}")
            print(f"   📈 Average Compliance: {total_score:.1f}%")
            print(f"   📁 Report: {report_file}")
            print(f"   📍 Full Path: {os.path.abspath(report_file)}")
            
            # Try to open the report
            print("\n🖥️  Attempting to open report in browser...")
            open_file_in_browser(report_path)
            
        else:
            print("\n❌ No devices were audited successfully")
            
    except Exception as e:
        print(f"❌ Error generating report: {e}")

if __name__ == "__main__":
    main()