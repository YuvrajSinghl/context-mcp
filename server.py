"""Entry point for the local context MCP server.

This file intentionally exposes a *single high-level orchestration tool* instead
of many low-level API-shaped tools.

Why expose only one high-level tool?
- Clients call this at session start and receive a coherent context bundle.
- A single entrypoint keeps client prompts simpler and reduces sequencing errors
  (e.g., fetching story data but forgetting related risks/open questions).
- We can evolve internal composition later without breaking MCP clients.

Why keep orchestration server-side?
- The server can enforce one deterministic flow for data assembly and shaping.
- Clients should not need to know integration ordering or transformation rules.
- Future concerns (auth, retries, caching, observability) belong at this
  boundary, not spread across every client implementation.

Why no write/delete operations?
- This server is currently read-only context preparation for coding sessions.
- Excluding mutations avoids accidental side effects on source systems.
- Read-only behavior is safer while integrations are still mocked and evolving.
"""

import json

from fastmcp import FastMCP

from tools.context_tool import build_context_tool

# Initialize the MCP server instance so it can be run locally via:
#   python server.py
mcp = FastMCP(name="context-mcp")


@mcp.tool(
    name="context.build_bundle",
    description=(
        "Use this tool at the beginning of a coding session when working on a "
        "Jira ticket. It gathers structured context before writing code."
    ),
)
def context_build_bundle(jira_key: str) -> dict:
    """Build a deterministic, JSON-serializable context bundle for one Jira key."""

    print(f"[context-mcp] tool=context.build_bundle jira_key={jira_key}")

    # Delegate to application logic (currently mocked/deterministic).
    bundle_dict = build_context_tool(jira_key=jira_key)

    # Enforce strict JSON serializability before returning through MCP.
    # `json.dumps` will raise if non-serializable types leak in.
    json_ready_bundle = json.loads(json.dumps(bundle_dict))

    print("[context-mcp] tool=context.build_bundle status=success")
    return json_ready_bundle


if __name__ == "__main__":
    print("[context-mcp] starting local MCP server")
    mcp.run()
