"""Entry point for the context MCP server.

This module wires transport concerns (MCP protocol exposure) to application
logic (context-building service). The comments are intentionally detailed so new
contributors can understand the request flow end-to-end.
"""

from fastmcp import FastMCP

from tools.context_tool import build_context_tool

# Create the MCP server instance. `FastMCP` manages protocol handshake, tool
# registration, argument validation, and response marshalling for us.
mcp = FastMCP(name="context-mcp")


@mcp.tool(name="context.build_bundle")
def context_build_bundle(jira_key: str) -> dict:
    """Tool entrypoint for building a context bundle from a Jira key.

    Flow overview:
    1. An MCP client invokes the `context.build_bundle` tool with `jira_key`.
    2. FastMCP validates/coerces the argument according to this signature.
    3. This handler delegates to `build_context_tool`, keeping server code thin.
    4. `build_context_tool` uses `ContextBuilder` to assemble structured context.
    5. A JSON-safe dictionary is returned through MCP back to the client.

    Keeping this wrapper small makes future migration easier when auth, tracing,
    retries, or caching are introduced at the server boundary.
    """

    return build_context_tool(jira_key=jira_key)


if __name__ == "__main__":
    # Run the MCP server when executed directly. This allows local development
    # via `python server.py` while still enabling import-based execution in tests
    # or when embedded by other launch mechanisms.
    mcp.run()
