from agents import trace


def get_trace_url(tr: trace) -> str:
    tracing_url = f"https://platform.openai.com/traces/trace?trace_id={tr.trace_id}"
    return tracing_url



# ...existing code...

from IPython.display import display, HTML
import json
from typing import List, Dict, Any

def display_agent_execution_steps(result, theme="dark"):
    """
    Display the execution steps of an agent in a nicely formatted HTML output.

    Args:
        result: The result object containing new_items with agent execution steps
        theme: "dark" or "light" theme option (default: "dark")
    """
    # Define theme-based styling
    if theme.lower() == "dark":
        styles = {
            "main_bg": "#2d2d2d",
            "header_bg": "#3c3c3c",
            "text_color": "#e0e0e0",
            "heading_color": "#61dafb",
            "strong_color": "#f0f0f0",
            "border_color": "#555",
            "json_bg": "#1e1e1e",
            "json_border": "#444",
            "json_text": "#d4d4d4",
            "tool_output_bg": "#1a2233",
            "tool_output_border": "#61dafb",
            "message_bg": "#1e331e",
            "message_border": "#4caf50",
            "step_type_color": "#61dafb"
        }
    else:  # light theme
        styles = {
            "main_bg": "#ffffff",
            "header_bg": "#f5f5f5",
            "text_color": "#333333",
            "heading_color": "#1a73e8",
            "strong_color": "#000000",
            "border_color": "#ddd",
            "json_bg": "#f8f8f8",
            "json_border": "#e0e0e0",
            "json_text": "#333333",
            "tool_output_bg": "#f0f7ff",
            "tool_output_border": "#1a73e8",
            "message_bg": "#f0fff0",
            "message_border": "#34a853",
            "step_type_color": "#1a73e8"
        }

    html = f"""
    <style>
        .agent-steps {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px 0;
            width: 100%;
            color: {styles["text_color"]};
        }}
        .step {{
            margin-bottom: 20px;
            border: 1px solid {styles["border_color"]};
            border-radius: 5px;
            overflow: hidden;
            background-color: {styles["main_bg"]};
        }}
        .step-header {{
            background-color: {styles["header_bg"]};
            padding: 10px;
            font-weight: bold;
            border-bottom: 1px solid {styles["border_color"]};
        }}
        .step-content {{
            padding: 15px;
            background-color: {styles["main_bg"]};
        }}
        .step-type {{
            color: {styles["step_type_color"]};
            display: inline-block;
            margin-right: 10px;
        }}
        .json-block {{
            background-color: {styles["json_bg"]};
            border: 1px solid {styles["json_border"]};
            border-radius: 3px;
            padding: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
            white-space: pre-wrap;
            margin-top: 10px;
            color: {styles["json_text"]};
        }}
        .tool-output {{
            background-color: {styles["tool_output_bg"]};
            border-left: 4px solid {styles["tool_output_border"]};
            padding: 10px;
            margin-top: 10px;
        }}
        .message-content {{
            background-color: {styles["message_bg"]};
            border-left: 4px solid {styles["message_border"]};
            padding: 10px;
            margin-top: 10px;
        }}
        .agent-steps h2 {{
            color: {styles["heading_color"]};
            margin-bottom: 15px;
        }}
        strong {{
            color: {styles["strong_color"]};
        }}
        .theme-toggle {{
            margin: 10px 0;
            text-align: right;
        }}
    </style>
    <div class="agent-steps">
        <div class="theme-toggle">
            <em>Current theme: {theme}</em>
        </div>
        <h2>Agent Execution Steps</h2>
    """

    for i, item in enumerate(result.new_items):
        item_type = item.type
        step_num = i + 1

        html += f"""
        <div class="step">
            <div class="step-header">
                <span class="step-type">{item_type}</span>
                <span>Step {step_num}</span>
            </div>
            <div class="step-content">
        """

        # Tool Call
        if item_type == 'tool_call_item':
            tool_name = item.raw_item.name
            tool_args = item.raw_item.arguments

            html += f"""
                <p><strong>Tool:</strong> {tool_name}</p>
                <p><strong>Arguments:</strong></p>
                <div class="json-block">{json.dumps(json.loads(tool_args), indent=2)}</div>
            """

        # Tool Output
        elif item_type == 'tool_call_output_item':
            if hasattr(item, 'output') and item.output:
                # Format the output based on the Weather class
                # html += f"""
                #     <p><strong>Tool Output:</strong></p>
                #     <div class="tool-output">
                #         <p>City: {item.output}</p>
                #         # <p>Temperature: {item.output.temperature}</p>
                #         # <p>Conditions: {item.output.conditions}</p>
                #     </div>
                # """
                html += f"""
                    <p><strong>Tool Output:</strong></p>
                    <div class="tool-output">
                        <p>Tool Output: {item.output}</p>
                    </div>
                """
            else:
                output_str = str(item.raw_item.get('output', 'No output'))
                html += f"""
                    <p><strong>Tool Output:</strong></p>
                    <div class="tool-output">{output_str}</div>
                """

        # Final Message
        elif item_type == 'message_output_item':
            message_content = ""
            if hasattr(item.raw_item, 'content'):
                for content_item in item.raw_item.content:
                    if hasattr(content_item, 'text'):
                        message_content += content_item.text

            html += f"""
                <p><strong>Assistant Response:</strong></p>
                <div class="message-content">{message_content}</div>
            """

        html += """
            </div>
        </div>
        """

    html += "</div>"

    return HTML(html)
