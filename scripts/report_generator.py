from jinja2 import Template
import os
from datetime import datetime

def generate_compliance_report(audit_results, template_path, output_path):
    """Generate HTML compliance report"""
    
    # Calculate overall statistics
    total_devices = len(audit_results)
    avg_compliance = sum(r['compliance_score'] for r in audit_results) / total_devices if total_devices > 0 else 0
    
    high_risk_issues = 0
    medium_risk_issues = 0
    
    for device in audit_results:
        for check_name, check_result in device['checks'].items():
            if not check_result['passed']:
                if check_result['severity'] == 'high':
                    high_risk_issues += 1
                elif check_result['severity'] == 'medium':
                    medium_risk_issues += 1
    
    summary = {
        'total_devices': total_devices,
        'avg_compliance': round(avg_compliance, 1),
        'high_risk_issues': high_risk_issues,
        'medium_risk_issues': medium_risk_issues,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Load and render template with proper encoding
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
    except UnicodeDecodeError:
        # Fallback to latin-1 if utf-8 fails
        with open(template_path, 'r', encoding='latin-1') as f:
            template = Template(f.read())
    
    html_output = template.render(
        devices=audit_results,
        summary=summary
    )
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save report with proper encoding
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"📊 Compliance report generated: {output_path}")
    return output_path