"""
Helper functions for the TrustyAI Shield Demo
Red Hat Summit Connect 2025
"""

from IPython.display import display, HTML, clear_output
import pandas as pd
from ipywidgets import widgets


class ShieldMetrics:
    """Track and display shield performance metrics"""

    def __init__(self):
        self.attempts = 0
        self.blocked = 0
        self.allowed = 0
        self.pii_types_detected = []

    def display(self):
        if self.attempts == 0:
            blocked_pct = 0
        else:
            blocked_pct = (self.blocked / self.attempts) * 100

        html = f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 10px; margin: 20px 0;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0; font-size: 24px;'>🛡️ Live Shield Performance</h3>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 15px;'>
                <div style='text-align: center;'>
                    <div style='font-size: 36px; font-weight: bold;'>{self.attempts}</div>
                    <div style='opacity: 0.9;'>Total Attempts</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 36px; font-weight: bold; color: #4caf50;'>{self.blocked}</div>
                    <div style='opacity: 0.9;'>🛡️ Blocked</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 36px; font-weight: bold;'>{blocked_pct:.0f}%</div>
                    <div style='opacity: 0.9;'>Block Rate</div>
                </div>
            </div>
        </div>
        """
        display(HTML(html))

    def record(self, blocked, pii_type=None):
        self.attempts += 1
        if blocked:
            self.blocked += 1
            if pii_type and pii_type not in self.pii_types_detected:
                self.pii_types_detected.append(pii_type)
        else:
            self.allowed += 1


def show_hero_banner():
    """Display the main demo banner"""
    display(HTML("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 40px; border-radius: 15px; text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2); margin: 20px 0;'>
        <h1 style='margin: 0; font-size: 48px;'>🛡️ Engineering Trustworthy AI</h1>
        <p style='font-size: 24px; margin-top: 15px; opacity: 0.95;'>The Decoupled Shield Pattern</p>
        <p style='font-size: 18px; margin-top: 10px; opacity: 0.9;'>TrustyAI + LlamaStack on OpenShift AI</p>
    </div>
    """))


def show_attack_surface(shield_config):
    """Visual representation of protection layers"""
    html = """
    <div style='font-family: monospace; margin: 20px 0;'>
    <div style='display: flex; align-items: center; margin: 10px 0;'>
        <div style='width: 120px; font-weight: bold; font-size: 14px;'>User Input</div>
        <div style='flex: 1; height: 3px; background: #ddd;'></div>
        {input_shield}
        <div style='flex: 1; height: 3px; background: #ddd;'></div>
        <div style='width: 100px; text-align: center; padding: 10px; background: #e3f2fd; border: 2px solid #2196f3; border-radius: 5px; font-size: 14px;'>🤖 Model</div>
        <div style='flex: 1; height: 3px; background: #ddd;'></div>
        {output_shield}
        <div style='flex: 1; height: 3px; background: #ddd;'></div>
        <div style='width: 120px; text-align: right; font-weight: bold; font-size: 14px;'>Response</div>
    </div>
    {legend}
    </div>
    """

    input_shield = "<div style='width: 80px; text-align: center; padding: 8px; background: #4caf50; color: white; border-radius: 5px; margin: 0 10px; font-size: 12px;'>🛡️ IN</div>" if \
    shield_config[
        'input'] else "<div style='width: 80px; text-align: center; padding: 8px; background: #f44336; color: white; border-radius: 5px; margin: 0 10px; font-size: 12px;'>❌ NONE</div>"

    output_shield = "<div style='width: 80px; text-align: center; padding: 8px; background: #4caf50; color: white; border-radius: 5px; margin: 0 10px; font-size: 12px;'>🛡️ OUT</div>" if \
    shield_config[
        'output'] else "<div style='width: 80px; text-align: center; padding: 8px; background: #f44336; color: white; border-radius: 5px; margin: 0 10px; font-size: 12px;'>❌ NONE</div>"

    legend = f"<div style='margin-top: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px;'><strong>Current Config:</strong> {shield_config['name']}</div>"

    display(HTML(html.format(input_shield=input_shield, output_shield=output_shield, legend=legend)))


def show_result_card(title, status, message, details=None):
    """Show a result card with color-coded status"""
    colors = {
        'blocked': {'bg': '#ffebee', 'border': '#f44336', 'text': '#c62828', 'icon': '🛡️'},
        'allowed': {'bg': '#e8f5e9', 'border': '#4caf50', 'text': '#2e7d32', 'icon': '✅'},
        'warning': {'bg': '#fff3cd', 'border': '#ffc107', 'text': '#856404', 'icon': '⚠️'},
        'error': {'bg': '#fff', 'border': '#f44336', 'text': '#c62828', 'icon': '❌'}
    }

    color = colors.get(status, colors['warning'])
    details_html = f"<div style='margin-top: 10px; color: #666; font-size: 14px;'>{details}</div>" if details else ""

    html = f"""
    <div style='background: {color['bg']}; border-left: 4px solid {color['border']}; 
                padding: 15px; margin: 10px 0; border-radius: 4px;'>
        <div style='color: {color['text']}; font-weight: bold; font-size: 18px;'>
            {color['icon']} {title}
        </div>
        <div style='margin-top: 8px; color: #555;'>{message}</div>
        {details_html}
    </div>
    """
    display(HTML(html))


def show_comparison_matrix():
    """Create a visual matrix showing protection levels"""

    scenarios = [
        ("Email PII", "john@example.com", False),
        ("SSN", "123-45-6789", False),
        ("Credit Card", "4532-1234-5678-9010", False),
        ("Multiple PII", "email + SSN + card", False),
        ("Safe Query", "How do I reset password?", True)
    ]

    html = """
    <style>
    .comparison-table { 
        width: 100%; 
        border-collapse: collapse; 
        margin: 20px 0; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 14px;
    }
    .comparison-table th { 
        background: #2c3e50; 
        color: white; 
        padding: 15px; 
        text-align: left;
    }
    .comparison-table td { 
        padding: 12px 15px; 
        border-bottom: 1px solid #ddd;
    }
    .comparison-table tr:hover { background: #f5f5f5; }
    .blocked { 
        background: #4caf50; 
        color: white; 
        padding: 5px 10px; 
        border-radius: 3px; 
        display: inline-block;
        font-weight: bold;
    }
    .allowed { 
        background: #f44336; 
        color: white; 
        padding: 5px 10px; 
        border-radius: 3px; 
        display: inline-block;
        font-weight: bold;
    }
    .partial {
        background: #ff9800;
        color: white;
        padding: 5px 10px;
        border-radius: 3px;
        display: inline-block;
        font-weight: bold;
    }
    .safe-allowed {
        background: #4caf50;
        color: white;
        padding: 5px 10px;
        border-radius: 3px;
        display: inline-block;
        font-weight: bold;
    }
    </style>
    <table class="comparison-table">
    <thead>
        <tr>
            <th>Attack Scenario</th>
            <th>No Shields</th>
            <th>Input Only</th>
            <th>Output Only</th>
            <th>Both (Recommended)</th>
        </tr>
    </thead>
    <tbody>
    """

    for scenario, example, is_safe in scenarios:
        if is_safe:
            html += f"""
            <tr>
                <td><strong>{scenario}</strong><br><small style='color: #666;'>{example}</small></td>
                <td><span class='safe-allowed'>✅ Allowed</span></td>
                <td><span class='safe-allowed'>✅ Allowed</span></td>
                <td><span class='safe-allowed'>✅ Allowed</span></td>
                <td><span class='safe-allowed'>✅ Allowed</span></td>
            </tr>
            """
        else:
            html += f"""
            <tr>
                <td><strong>{scenario}</strong><br><small style='color: #666;'>{example}</small></td>
                <td><span class='allowed'>❌ EXPOSED</span></td>
                <td><span class='blocked'>🛡️ Blocked</span></td>
                <td><span class='partial'>⚠️ Partial</span></td>
                <td><span class='blocked'>🛡️ Blocked</span></td>
            </tr>
            """

    html += """
    </tbody>
    </table>
    <div style='margin-top: 20px; padding: 15px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px;'>
        <strong>⚡ Key Insight:</strong> Defense-in-depth with both input and output shields provides complete protection while maintaining functionality for safe queries.
    </div>
    """

    display(HTML(html))


def show_compliance_savings():
    """Show financial impact of preventing data breaches"""
    html = """
    <div style='background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;'>
        <h3 style='color: #2c3e50; margin-top: 0;'>💰 Real-World Impact</h3>
        <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;'>
            <div style='background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #e74c3c;'>
                <div style='font-size: 32px; font-weight: bold; color: #e74c3c;'>$4.88M</div>
                <div style='color: #666; margin-top: 5px;'>Average cost of a data breach (IBM 2024)</div>
            </div>
            <div style='background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60;'>
                <div style='font-size: 32px; font-weight: bold; color: #27ae60;'>2-3 weeks</div>
                <div style='color: #666; margin-top: 5px;'>Development time saved per agent</div>
            </div>
            <div style='background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db;'>
                <div style='font-size: 32px; font-weight: bold; color: #3498db;'>1 shield</div>
                <div style='color: #666; margin-top: 5px;'>Protects unlimited agents</div>
            </div>
            <div style='background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #9b59b6;'>
                <div style='font-size: 32px; font-weight: bold; color: #9b59b6;'>Zero</div>
                <div style='color: #666; margin-top: 5px;'>Code changes to update shields</div>
            </div>
        </div>
    </div>
    """
    display(HTML(html))


def create_interactive_tester(client):
    """Let audience try their own prompts"""
    output = widgets.Output()

    text_input = widgets.Textarea(
        value='',
        placeholder='Enter a test message (try including an email or SSN)...',
        description='',
        layout=widgets.Layout(width='100%', height='80px')
    )

    button = widgets.Button(
        description='🛡️ Test with Shield',
        button_style='primary',
        layout=widgets.Layout(width='200px')
    )

    def on_button_click(b):
        with output:
            clear_output()
            if not text_input.value.strip():
                print("⚠️ Please enter a message to test")
                return

            print(f"Testing: {text_input.value[:60]}...\n")

            try:
                result = client.safety.run_shield(
                    shield_id="pii_shield",
                    messages=[{"role": "user", "content": text_input.value}],
                    params={}
                )

                if result.violation:
                    display(HTML(f"""
                    <div style='background: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 10px 0; border-radius: 4px;'>
                        <div style='color: #c62828; font-weight: bold; font-size: 18px;'>🛡️ BLOCKED</div>
                        <div style='margin-top: 10px; color: #666;'>{result.violation.user_message}</div>
                    </div>
                    """))
                else:
                    display(HTML(f"""
                    <div style='background: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; margin: 10px 0; border-radius: 4px;'>
                        <div style='color: #2e7d32; font-weight: bold; font-size: 18px;'>✅ ALLOWED</div>
                        <div style='margin-top: 10px; color: #666;'>Message passed all shield checks</div>
                    </div>
                    """))
            except Exception as e:
                print(f"❌ Error: {e}")

    button.on_click(on_button_click)

    display(HTML("<h3>🎮 Interactive Shield Tester</h3><p>Enter any message to see TrustyAI shields in action:</p>"))
    display(text_input)
    display(button)
    display(output)


# Test data definitions
TEST_PROMPTS = {
    "normal": {
        "prompt": "How do I reset my password?",
        "risk": "None",
        "pii_type": None
    },
    "pii_email": {
        "prompt": "I can't log in. My email is john.doe@acme.com and I need help.",
        "risk": "Email",
        "pii_type": "email"
    },
    "pii_ssn": {
        "prompt": "My SSN is 123-45-6789. Can you verify my account?",
        "risk": "SSN",
        "pii_type": "ssn"
    },
    "pii_credit_card": {
        "prompt": "My credit card 4532-1234-5678-9010 isn't working. Please help.",
        "risk": "Credit Card",
        "pii_type": "credit_card"
    },
    "pii_multiple": {
        "prompt": "Hi, I'm having issues. My email is jane@company.com, SSN is 987-65-4321, and card 5105-1051-0510-5100.",
        "risk": "Multiple PII",
        "pii_type": "multiple"
    }
}

SHIELD_CONFIG = {
    "shield_id": "pii_shield",
    "provider_shield_id": "pii_shield",
    "provider_id": "trustyai_fms",
    "params": {
        "type": "content",
        "confidence_threshold": 0.8,
        "message_types": ["user", "system", "tool", "completion"],
        "detectors": {
            "regex": {
                "detector_params": {
                    "regex": ["email", "ssn", "credit-card"]
                }
            }
        }
    }
}