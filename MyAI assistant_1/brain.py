import json
from duckduckgo_search import DDGS
from security import safe_execute  # <-- actually use it

class AssistantTools:
    @staticmethod
    def web_search(query: str) -> str:
        """Search the internet for current information."""
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            return "\n".join(r["body"] for r in results)

    @staticmethod
    def run_command(command: str) -> str:
        """Execute a whitelisted command only — routed through security.py."""
        return safe_execute(command)

    @staticmethod
    def open_application(app_name: str) -> str:
        """Open an application, validated against the whitelist."""
        return safe_execute(f"open {app_name}")