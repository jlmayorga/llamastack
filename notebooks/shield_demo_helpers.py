"""
Helper functions for the TrustyAI Shield Demo
Red Hat Summit Connect 2025

Enhanced version with better error handling, improved visuals, and additional features.
"""

from IPython.display import display, HTML, clear_output
import pandas as pd
from ipywidgets import widgets
from typing import Optional, Dict, List


class ShieldMetrics:
    """Track and display shield performance metrics"""

    def __init__(self):
        self.attempts = 0
        self.blocked = 0
        self.allowed = 0
        self.pii_types_detected = []

    def record(self, blocked: bool, pii_type: Optional[str] = None):
        """Record a shield attempt"""
        self.attempts += 1
        if blocked:
            self.blocked += 1
            if pii_type and pii_type not in self.pii_types_detected:
                self.pii_types_detected.append(pii_type)
        else:
            self.allowed += 1

    def display(self):
        """Display current metrics"""
        if self.attempts == 0:
            blocked_pct = 0
            protection_score = 0
        else:
            blocked_pct = (self.blocked / self.attempts) * 100
            # Calculate protection score (higher is better for risky prompts)
            protection_score = min(100, blocked_pct * 1.2)

        html = f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 25px; border-radius: 12px; margin: 20px 0;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.15);'>
            <h3 style='margin-top: 0; font-size: 26px; font-weight: 600;'>
                🛡️ Live Shield Performance Metrics
            </h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); 
                        gap: 20px; margin-top: 20px;'>
                <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 8px; 
                            backdrop-filter: blur(10px);'>
                    <div style='font-size: 42px; font-weight: bold;'>{self.attempts}</div>
                    <div style='opacity: 0.95; margin-top: 5px; font-size: 14px;'>Total Attempts</div>
                </div>
                <div style='background: rgba(76,175,80,0.2); padding: 20px; border-radius: 8px;
                            border: 2px solid rgba(76,175,80,0.4);'>
                    <div style='font-size: 42px; font-weight: bold; color: #4caf50;'>{self.blocked}</div>
                    <div style='opacity: 0.95; margin-top: 5px; font-size: 14px;'>🛡️ Blocked</div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 8px;
                            backdrop-filter: blur(10px);'>
                    <div style='font-size: 42px; font-weight: bold;'>{blocked_pct:.0f}%</div>
                    <div style='opacity: 0.95; margin-top: 5px; font-size: 14px;'>Block Rate</div>
                </div>
                <div style='background: rgba(255,193,7,0.2); padding: 20px; border-radius: 8px;
                            border: 2px solid rgba(255,193,7,0.4);'>
                    <div style='font-size: 42px; font-weight: bold; color: #ffc107;'>{protection_score:.0f}</div>
                    <div style='opacity: 0.95; margin-top: 5px; font-size: 14px;'>Protection Score</div>
                </div>
            </div>
            {self._get_pii_breakdown()}
        </div>
        """
        display(HTML(html))

    def _get_pii_breakdown(self) -> str:
        """Generate HTML for PII types detected"""
        if not self.pii_types_detected:
            return ""

        pii_badges = "".join([
            f"<span style='background: rgba(255,255,255,0.3); padding: 6px 12px; "
            f"border-radius: 16px; margin: 4px; display: inline-block; font-size: 13px;'>"
            f"{pii_type.replace('_', ' ').title()}</span>"
            for pii_type in self.pii_types_detected
        ])

        return f"""
        <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);'>
            <div style='font-size: 14px; opacity: 0.9; margin-bottom: 10px;'>
                🔍 PII Types Detected:
            </div>
            <div>{pii_badges}</div>
        </div>
        """


def show_hero_banner():
    """Display the main demo banner"""
    display(HTML("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 50px 40px; border-radius: 16px; text-align: center;
                box-shadow: 0 12px 32px rgba(0,0,0,0.25); margin: 25px 0;
                border: 1px solid rgba(255,255,255,0.1);'>
        <div style='font-size: 56px; margin-bottom: 10px;'>🛡️</div>
        <h1 style='margin: 0; font-size: 52px; font-weight: 700; line-height: 1.2;'>
            Engineering Trustworthy AI
        </h1>
        <p style='font-size: 28px; margin-top: 20px; opacity: 0.95; font-weight: 400;'>
            The Decoupled Shield Pattern
        </p>
        <p style='font-size: 20px; margin-top: 15px; opacity: 0.85; font-weight: 300;'>
            TrustyAI + LlamaStack on OpenShift AI
        </p>
        <div style='margin-top: 25px; padding-top: 25px; border-top: 1px solid rgba(255,255,255,0.2);
                    font-size: 16px; opacity: 0.8;'>
            Red Hat Summit Connect 2025
        </div>
    </div>
    """))


def show_problem_statement():
    """Display the problem statement"""
    display(HTML("""
    <div style='background: #fff3cd; border-left: 5px solid #ffc107; padding: 25px; 
                margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <h3 style='margin-top: 0; color: #856404; font-size: 24px;'>
            ⚠️ The Trust Gap Problem
        </h3>
        <p style='color: #666; font-size: 16px; line-height: 1.6; margin: 15px 0;'>
            Your AI agents are helpful and fast, but what happens when users accidentally 
            share sensitive data like emails, SSNs, or credit cards?
        </p>
        <div style='background: white; padding: 15px; border-radius: 6px; margin-top: 15px;'>
            <strong style='color: #856404;'>Without Protection:</strong>
            <ul style='margin: 10px 0; padding-left: 20px; color: #666;'>
                <li>PII flows into logs, databases, and training data</li>
                <li>No way to audit sensitive data exposure</li>
                <li>Compliance violations (GDPR, HIPAA, PCI-DSS)</li>
                <li>Average breach cost: <strong>$4.88M</strong></li>
            </ul>
        </div>
    </div>
    """))


def show_attack_surface(shield_config: Dict[str, any]):
    """Visual representation of protection layers"""

    input_shield = (
        "<div style='width: 90px; text-align: center; padding: 10px; background: #4caf50; "
        "color: white; border-radius: 6px; margin: 0 10px; font-size: 13px; font-weight: 600; "
        "box-shadow: 0 2px 6px rgba(76,175,80,0.3);'>🛡️ IN</div>"
        if shield_config['input'] else
        "<div style='width: 90px; text-align: center; padding: 10px; background: #f44336; "
        "color: white; border-radius: 6px; margin: 0 10px; font-size: 13px; font-weight: 600; "
        "box-shadow: 0 2px 6px rgba(244,67,54,0.3);'>❌ NONE</div>"
    )

    output_shield = (
        "<div style='width: 90px; text-align: center; padding: 10px; background: #4caf50; "
        "color: white; border-radius: 6px; margin: 0 10px; font-size: 13px; font-weight: 600; "
        "box-shadow: 0 2px 6px rgba(76,175,80,0.3);'>🛡️ OUT</div>"
        if shield_config['output'] else
        "<div style='width: 90px; text-align: center; padding: 10px; background: #f44336; "
        "color: white; border-radius: 6px; margin: 0 10px; font-size: 13px; font-weight: 600; "
        "box-shadow: 0 2px 6px rgba(244,67,54,0.3);'>❌ NONE</div>"
    )

    # Calculate protection level
    protection_icons = ""
    if shield_config['input'] and shield_config['output']:
        protection_level = "Maximum Security 🔒"
        protection_color = "#4caf50"
        protection_icons = "🛡️🛡️"
    elif shield_config['input'] or shield_config['output']:
        protection_level = "Partial Protection ⚠️"
        protection_color = "#ff9800"
        protection_icons = "🛡️"
    else:
        protection_level = "No Protection ❌"
        protection_color = "#f44336"
        protection_icons = "⚠️"

    html = f"""
    <div style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
                margin: 25px 0; padding: 25px; background: #f8f9fa; border-radius: 12px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);'>
        <div style='margin-bottom: 20px; text-align: center;'>
            <div style='display: inline-block; background: {protection_color}; color: white; 
                        padding: 10px 20px; border-radius: 20px; font-size: 16px; font-weight: 600;'>
                {protection_icons} {shield_config['name']}
            </div>
        </div>
        <div style='display: flex; align-items: center; justify-content: center; margin: 20px 0;'>
            <div style='min-width: 140px; font-weight: 600; font-size: 15px; text-align: right;
                        color: #333;'>
                👤 User Input
            </div>
            <div style='flex: 0 0 60px; height: 3px; background: linear-gradient(to right, #ddd, #bbb);'></div>
            {input_shield}
            <div style='flex: 0 0 60px; height: 3px; background: linear-gradient(to right, #bbb, #ddd);'></div>
            <div style='min-width: 120px; text-align: center; padding: 15px; background: #e3f2fd; 
                        border: 2px solid #2196f3; border-radius: 8px; font-size: 15px; font-weight: 600;
                        color: #1976d2; box-shadow: 0 2px 6px rgba(33,150,243,0.2);'>
                🤖 Model
            </div>
            <div style='flex: 0 0 60px; height: 3px; background: linear-gradient(to right, #ddd, #bbb);'></div>
            {output_shield}
            <div style='flex: 0 0 60px; height: 3px; background: linear-gradient(to right, #bbb, #ddd);'></div>
            <div style='min-width: 140px; text-align: left; font-weight: 600; font-size: 15px;
                        color: #333;'>
                💬 Response
            </div>
        </div>
        <div style='margin-top: 20px; padding: 15px; background: white; border-radius: 8px;
                    border-left: 4px solid {protection_color};'>
            <strong style='color: {protection_color};'>Protection Level:</strong> 
            <span style='color: #666;'>{protection_level}</span>
        </div>
    </div>
    """

    display(HTML(html))


def show_result_card(title: str, status: str, message: str, details: Optional[str] = None):
    """Show a result card with color-coded status"""
    colors = {
        'blocked': {
            'bg': '#ffebee', 'border': '#f44336', 'text': '#c62828',
            'icon': '🛡️', 'title_bg': '#f44336'
        },
        'allowed': {
            'bg': '#e8f5e9', 'border': '#4caf50', 'text': '#2e7d32',
            'icon': '✅', 'title_bg': '#4caf50'
        },
        'warning': {
            'bg': '#fff3cd', 'border': '#ffc107', 'text': '#856404',
            'icon': '⚠️', 'title_bg': '#ffc107'
        },
        'error': {
            'bg': '#ffebee', 'border': '#f44336', 'text': '#c62828',
            'icon': '❌', 'title_bg': '#f44336'
        }
    }

    color = colors.get(status, colors['warning'])
    details_html = (
        f"<div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid {color['border']}30; "
        f"color: #555; font-size: 15px; line-height: 1.6;'>{details}</div>"
        if details else ""
    )

    html = f"""
    <div style='background: {color['bg']}; border-left: 5px solid {color['border']}; 
                padding: 20px; margin: 15px 0; border-radius: 8px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
            <div style='font-size: 32px;'>{color['icon']}</div>
            <div style='color: {color['text']}; font-weight: 700; font-size: 20px; flex: 1;'>
                {title}
            </div>
        </div>
        <div style='color: #444; font-size: 16px; line-height: 1.6; margin-left: 44px;'>
            {message}
        </div>
        {details_html}
    </div>
    """
    display(HTML(html))


def show_comparison_matrix():
    """Create a visual matrix showing protection levels"""

    scenarios = [
        ("📧 Email PII", "john@example.com", False, "high"),
        ("🔢 SSN", "123-45-6789", False, "critical"),
        ("💳 Credit Card", "4532-1234-5678-9010", False, "critical"),
        ("📋 Multiple PII", "email + SSN + card", False, "critical"),
        ("✅ Safe Query", "How do I reset password?", True, "none")
    ]

    html = """
    <style>
    .comparison-table { 
        width: 100%; 
        border-collapse: separate;
        border-spacing: 0;
        margin: 25px 0; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-size: 15px;
        border-radius: 8px;
        overflow: hidden;
    }
    .comparison-table th { 
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white; 
        padding: 18px 15px; 
        text-align: left;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .comparison-table td { 
        padding: 16px 15px; 
        border-bottom: 1px solid #eee;
        background: white;
    }
    .comparison-table tr:last-child td {
        border-bottom: none;
    }
    .comparison-table tr:hover td { 
        background: #f8f9fa; 
    }
    .blocked { 
        background: #4caf50; 
        color: white; 
        padding: 6px 14px; 
        border-radius: 16px; 
        display: inline-block;
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 2px 4px rgba(76,175,80,0.3);
    }
    .allowed { 
        background: #f44336; 
        color: white; 
        padding: 6px 14px; 
        border-radius: 16px; 
        display: inline-block;
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 2px 4px rgba(244,67,54,0.3);
    }
    .partial {
        background: #ff9800;
        color: white;
        padding: 6px 14px;
        border-radius: 16px;
        display: inline-block;
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 2px 4px rgba(255,152,0,0.3);
    }
    .safe-allowed {
        background: #4caf50;
        color: white;
        padding: 6px 14px;
        border-radius: 16px;
        display: inline-block;
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 2px 4px rgba(76,175,80,0.3);
    }
    .risk-badge {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
        margin-left: 8px;
    }
    .risk-critical { background: #ffebee; color: #c62828; }
    .risk-high { background: #fff3cd; color: #856404; }
    .risk-none { background: #e8f5e9; color: #2e7d32; }
    </style>
    <table class="comparison-table">
    <thead>
        <tr>
            <th style='width: 25%;'>Attack Scenario</th>
            <th style='width: 18.75%; text-align: center;'>No Shields</th>
            <th style='width: 18.75%; text-align: center;'>Input Only</th>
            <th style='width: 18.75%; text-align: center;'>Output Only</th>
            <th style='width: 18.75%; text-align: center;'>Both (Recommended)</th>
        </tr>
    </thead>
    <tbody>
    """

    for scenario, example, is_safe, risk_level in scenarios:
        risk_badge = f"<span class='risk-badge risk-{risk_level}'>{risk_level}</span>"

        if is_safe:
            html += f"""
            <tr>
                <td>
                    <strong style='font-size: 15px;'>{scenario}</strong>{risk_badge}<br>
                    <small style='color: #999; font-size: 13px;'>{example}</small>
                </td>
                <td style='text-align: center;'><span class='safe-allowed'>✅ Allowed</span></td>
                <td style='text-align: center;'><span class='safe-allowed'>✅ Allowed</span></td>
                <td style='text-align: center;'><span class='safe-allowed'>✅ Allowed</span></td>
                <td style='text-align: center;'><span class='safe-allowed'>✅ Allowed</span></td>
            </tr>
            """
        else:
            html += f"""
            <tr>
                <td>
                    <strong style='font-size: 15px;'>{scenario}</strong>{risk_badge}<br>
                    <small style='color: #999; font-size: 13px;'>{example}</small>
                </td>
                <td style='text-align: center;'><span class='allowed'>❌ EXPOSED</span></td>
                <td style='text-align: center;'><span class='blocked'>🛡️ Blocked</span></td>
                <td style='text-align: center;'><span class='partial'>⚠️ Partial</span></td>
                <td style='text-align: center;'><span class='blocked'>🛡️ Blocked</span></td>
            </tr>
            """

    html += """
    </tbody>
    </table>
    <div style='margin-top: 25px; padding: 20px; background: #e3f2fd; border-left: 5px solid #2196f3; 
                border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
        <div style='font-weight: 600; color: #1565c0; font-size: 17px; margin-bottom: 10px;'>
            ⚡ Key Insight
        </div>
        <div style='color: #555; font-size: 15px; line-height: 1.6;'>
            Defense-in-depth with <strong>both input and output shields</strong> provides complete 
            protection while maintaining full functionality for legitimate business queries.
        </div>
    </div>
    """

    display(HTML(html))


def show_compliance_savings():
    """Show financial impact of preventing data breaches"""
    html = """
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 30px; border-radius: 12px; margin: 25px 0;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);'>
        <h3 style='color: #2c3e50; margin-top: 0; font-size: 28px; font-weight: 700;'>
            💰 Real-World Business Impact
        </h3>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
                    gap: 20px; margin-top: 25px;'>
            <div style='background: white; padding: 25px; border-radius: 10px; 
                        border-left: 5px solid #e74c3c; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                <div style='font-size: 40px; font-weight: 700; color: #e74c3c; margin-bottom: 8px;'>
                    $4.88M
                </div>
                <div style='color: #666; font-size: 15px; line-height: 1.5;'>
                    Average cost of a data breach<br>
                    <small style='color: #999;'>(IBM Security Report 2024)</small>
                </div>
            </div>
            <div style='background: white; padding: 25px; border-radius: 10px; 
                        border-left: 5px solid #27ae60; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                <div style='font-size: 40px; font-weight: 700; color: #27ae60; margin-bottom: 8px;'>
                    2-3 weeks
                </div>
                <div style='color: #666; font-size: 15px; line-height: 1.5;'>
                    Development time saved<br>
                    <small style='color: #999;'>(per AI agent deployed)</small>
                </div>
            </div>
            <div style='background: white; padding: 25px; border-radius: 10px; 
                        border-left: 5px solid #3498db; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                <div style='font-size: 40px; font-weight: 700; color: #3498db; margin-bottom: 8px;'>
                    1 shield
                </div>
                <div style='color: #666; font-size: 15px; line-height: 1.5;'>
                    Protects unlimited agents<br>
                    <small style='color: #999;'>(true reusability)</small>
                </div>
            </div>
            <div style='background: white; padding: 25px; border-radius: 10px; 
                        border-left: 5px solid #9b59b6; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                <div style='font-size: 40px; font-weight: 700; color: #9b59b6; margin-bottom: 8px;'>
                    Zero
                </div>
                <div style='color: #666; font-size: 15px; line-height: 1.5;'>
                    Code changes to update<br>
                    <small style='color: #999;'>(config-driven shields)</small>
                </div>
            </div>
        </div>
        <div style='margin-top: 25px; padding: 20px; background: rgba(255,255,255,0.9); 
                    border-radius: 8px;'>
            <div style='font-weight: 600; color: #2c3e50; margin-bottom: 12px; font-size: 16px;'>
                📊 ROI Calculation Example
            </div>
            <div style='color: #666; font-size: 14px; line-height: 1.8;'>
                <strong>Traditional Approach:</strong> 10 agents × 3 weeks development = 30 weeks<br>
                <strong>Shield Pattern:</strong> 1 shield + (10 agents × 2 days) = 1 week total<br>
                <strong style='color: #27ae60;'>Time Saved: 29 weeks (96% reduction)</strong>
            </div>
        </div>
    </div>
    """
    display(HTML(html))


def create_interactive_tester(client, model_name: str = "tinyllama-1b"):
    """Interactive shield tester with enhanced UI"""
    output = widgets.Output()

    text_input = widgets.Textarea(
        value='',
        placeholder='Try entering an email, SSN, credit card, or a safe message...',
        description='',
        layout=widgets.Layout(width='100%', height='100px')
    )

    button = widgets.Button(
        description='🛡️ Test Shield',
        button_style='primary',
        layout=widgets.Layout(width='180px', height='45px')
    )

    clear_button = widgets.Button(
        description='🔄 Clear',
        button_style='',
        layout=widgets.Layout(width='120px', height='45px')
    )

    # Example buttons
    example_safe = widgets.Button(
        description='📝 Safe Example',
        button_style='info',
        layout=widgets.Layout(width='150px')
    )

    example_email = widgets.Button(
        description='📧 Email PII',
        button_style='warning',
        layout=widgets.Layout(width='150px')
    )

    example_ssn = widgets.Button(
        description='🔢 SSN PII',
        button_style='warning',
        layout=widgets.Layout(width='150px')
    )

    def on_button_click(b):
        with output:
            clear_output()
            if not text_input.value.strip():
                display(HTML("""
                <div style='background: #fff3cd; border-left: 4px solid #ffc107; 
                            padding: 15px; border-radius: 4px;'>
                    <strong>⚠️ No input provided</strong><br>
                    Please enter a message to test
                </div>
                """))
                return

            display(HTML(f"""
            <div style='padding: 15px; background: #f8f9fa; border-radius: 8px; 
                        margin-bottom: 15px;'>
                <strong>Testing:</strong> {text_input.value[:80]}
                {'...' if len(text_input.value) > 80 else ''}
            </div>
            """))

            try:
                result = client.safety.run_shield(
                    shield_id="pii_shield",
                    messages=[{"role": "user", "content": text_input.value}],
                    params={}
                )

                if result.violation:
                    display(HTML(f"""
                    <div style='background: #ffebee; border-left: 5px solid #f44336; 
                                padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
                            <div style='font-size: 32px;'>🛡️</div>
                            <div style='color: #c62828; font-weight: 700; font-size: 20px;'>
                                BLOCKED BY SHIELD
                            </div>
                        </div>
                        <div style='margin-left: 44px; color: #555; line-height: 1.6;'>
                            <strong>Reason:</strong> {result.violation.user_message}<br>
                            <strong>Action:</strong> Message was not processed by the model
                        </div>
                    </div>
                    """))
                else:
                    display(HTML("""
                    <div style='background: #e8f5e9; border-left: 5px solid #4caf50; 
                                padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
                            <div style='font-size: 32px;'>✅</div>
                            <div style='color: #2e7d32; font-weight: 700; font-size: 20px;'>
                                ALLOWED
                            </div>
                        </div>
                        <div style='margin-left: 44px; color: #555; line-height: 1.6;'>
                            Message passed all shield checks and would be processed normally
                        </div>
                    </div>
                    """))
            except Exception as e:
                display(HTML(f"""
                <div style='background: #ffebee; border-left: 4px solid #f44336; 
                            padding: 15px; border-radius: 4px;'>
                    <strong>❌ Error:</strong> {str(e)[:200]}
                </div>
                """))

    def on_clear_click(b):
        text_input.value = ''
        with output:
            clear_output()

    def load_example(example_text):
        text_input.value = example_text

    button.on_click(on_button_click)
    clear_button.on_click(on_clear_click)
    example_safe.on_click(lambda b: load_example("How do I reset my password?"))
    example_email.on_click(lambda b: load_example("My email is test@example.com"))
    example_ssn.on_click(lambda b: load_example("My SSN is 123-45-6789"))

    display(HTML("""
    <h3 style='color: #2c3e50; margin-top: 30px;'>🎮 Interactive Shield Tester</h3>
    <p style='color: #666; font-size: 15px; margin-bottom: 20px;'>
        Enter any message to see TrustyAI shields in action. Try including sensitive data 
        like emails, SSNs, or credit cards to see how they're detected and blocked.
    </p>
    """))

    # Example buttons
    display(widgets.HBox([
        widgets.HTML("<strong style='margin-right: 10px;'>Quick Examples:</strong>"),
        example_safe,
        example_email,
        example_ssn
    ]))

    display(HTML("<div style='height: 15px;'></div>"))
    display(text_input)
    display(HTML("<div style='height: 10px;'></div>"))
    display(widgets.HBox([button, clear_button]))
    display(HTML("<div style='height: 15px;'></div>"))
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