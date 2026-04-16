# ANSI color codes for terminal output
from langchain_core.messages import BaseMessage


class TerminalColors:
    """ANSI color codes for colored terminal output."""
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_RED = '\033[41m'


def render_message_colored(message: BaseMessage, show_tool_calls: bool = True) -> str:
    """Render a LangChain message with colored formatting for terminal output."""
    msg_type = message.type
    content = message.content if message.content else ""
    output_lines = []

    if msg_type == "ai":
        header = f"{TerminalColors.BOLD}{TerminalColors.BLUE}🤖 AI Assistant{TerminalColors.RESET}"
        output_lines.append("=" * 100)
        output_lines.append(header)
        output_lines.append("=" * 100)
        if content:
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        text_content = block.get('text', '')
                        if text_content:
                            output_lines.append(f"{TerminalColors.CYAN}{text_content}{TerminalColors.RESET}")
            else:
                output_lines.append(f"{TerminalColors.CYAN}{content}{TerminalColors.RESET}")
        if show_tool_calls and hasattr(message, 'tool_calls') and message.tool_calls:
            output_lines.append(f"\n{TerminalColors.YELLOW}📞 Tool Calls ({len(message.tool_calls)}):{TerminalColors.RESET}")
            for i, tool_call in enumerate(message.tool_calls, 1):
                tool_name = tool_call.get('name', 'unknown')
                tool_args = tool_call.get('args', {})
                if i > 1:
                    output_lines.append("")
                output_lines.append(f"  {TerminalColors.BOLD}{TerminalColors.YELLOW}[{i}] {tool_name}{TerminalColors.RESET}")
                if tool_args:
                    for key, value in tool_args.items():
                        value_str = str(value)
                        if len(value_str) > 100:
                            value_str = value_str[:45] + " ... " + value_str[-45:]
                        output_lines.append(f"      {TerminalColors.GRAY}{key}:{TerminalColors.RESET} {value_str}")
                else:
                    output_lines.append(f"      {TerminalColors.GRAY}(no arguments){TerminalColors.RESET}")

    elif msg_type == "human":
        header = f"{TerminalColors.BOLD}{TerminalColors.GREEN}👤 Human{TerminalColors.RESET}"
        output_lines.append("=" * 100)
        output_lines.append(header)
        output_lines.append("=" * 100)
        output_lines.append(f"{TerminalColors.GREEN}{content}{TerminalColors.RESET}")

    elif msg_type == "tool":
        header = f"{TerminalColors.BOLD}{TerminalColors.MAGENTA}🔧 Tool Response{TerminalColors.RESET}"
        tool_name = getattr(message, 'name', 'unknown')
        output_lines.append("=" * 100)
        output_lines.append(f"{header} {TerminalColors.GRAY}({tool_name}){TerminalColors.RESET}")
        output_lines.append("=" * 100)
        if isinstance(content, list):
            text_parts = []
            image_count = 0
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'text':
                        text_parts.append(block.get('text', ''))
                    elif block.get('type') in ('image', 'image_url'):
                        image_count += 1
                elif isinstance(block, str):
                    text_parts.append(block)
            content = "\n".join(text_parts)
            if image_count:
                content += f"\n[{image_count} image(s) attached]"
        if isinstance(content, str) and len(content) > 10000:
            content = content[:4000].rstrip() + "\n\n... [middle content truncated] ...\n\n" + content[-4000:].lstrip()
        output_lines.append(f"{TerminalColors.MAGENTA}{content}{TerminalColors.RESET}")

    elif msg_type == "system":
        header = f"{TerminalColors.BOLD}{TerminalColors.YELLOW}⚙️  System{TerminalColors.RESET}"
        output_lines.append("=" * 100)
        output_lines.append(header)
        output_lines.append("=" * 100)
        output_lines.append(f"{TerminalColors.YELLOW}{content}{TerminalColors.RESET}")

    else:
        header = f"{TerminalColors.BOLD}{TerminalColors.WHITE}📝 {msg_type.upper()}{TerminalColors.RESET}"
        output_lines.append("=" * 100)
        output_lines.append(header)
        output_lines.append("=" * 100)
        output_lines.append(f"{TerminalColors.WHITE}{content}{TerminalColors.RESET}")

    output_lines.append("")
    return "\n".join(output_lines)
