"""Story models used by the context-building pipeline."""

from datetime import date

from pydantic import BaseModel, Field


class JiraStory(BaseModel):
    """Normalized Jira story data used across MCP tools.

    Keeping this as a dedicated model gives us strict, typed structure so every
    downstream consumer (including LLM tools) receives the same predictable keys.
    """

    # The canonical Jira issue key (for example: PROJ-123). This is the stable
    # identifier used to correlate the story across Jira, GitHub, and any logs.
    key: str = Field(..., description="Jira issue key, such as PROJ-123")

    # A concise one-line summary of the work item. This acts as the quickest
    # intent signal for Copilot and other assistants to anchor generated code.
    title: str = Field(..., description="Human-readable story title")

    # Rich narrative details for the task: acceptance criteria, scope boundaries,
    # and business rationale. LLMs rely heavily on this field to avoid guessing.
    description: str = Field(..., description="Detailed story description")

    # Optional target completion date. It can influence prioritization or urgency
    # hints, but remains optional because many Jira workflows do not set one.
    deadline: date | None = Field(
        default=None,
        description="Optional story deadline in YYYY-MM-DD format",
    )

    # Optional owner display name or identifier. This supports personalized
    # routing and collaboration context while allowing unassigned backlog items.
    assignee: str | None = Field(
        default=None,
        description="Optional assignee name or handle",
    )
