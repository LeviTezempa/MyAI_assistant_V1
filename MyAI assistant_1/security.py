import shlex
import subprocess

ALLOWED_COMMANDS = {
    "open": ["notepad", "calc", "chrome"],
    "dir": ["ls", "dir"],
}

def safe_execute(command: str):
    parts = shlex.split(command.lower())
    if not parts:
        return "Empty command."
    base = parts[0]

    if base not in ALLOWED_COMMANDS:
        return "Command not allowed for security."

    # Actually enforce the second-token whitelist
    if len(parts) > 1 and parts[1] not in ALLOWED_COMMANDS[base]:
        return "Argument not allowed for security."

    try:
        result = subprocess.run(parts, capture_output=True, text=True, timeout=10)
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)