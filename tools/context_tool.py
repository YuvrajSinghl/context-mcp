"""MCP-facing tool wrappers for context generation."""

from services.context_builder import ContextBuilder


def build_context_tool(jira_key: str) -> dict:
    """Build context for a Jira key and return JSON-serializable output."""

    builder = ContextBuilder()
    bundle = builder.build_bundle(jira_key=jira_key)
    return bundle.model_dump(mode="json")
