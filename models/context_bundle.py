"""Composite payload returned by the context-building tool."""

from pydantic import BaseModel, Field

from models.story import JiraStory


class ContextBundle(BaseModel):
    """Unified context package for coding assistants.

    The structure is intentionally explicit: Copilot-style agents perform better
    when context is grouped by semantic purpose instead of one large text blob.
    Separate fields help rank relevance and reduce hallucinated assumptions.
    """

    # Core source-of-truth story metadata. This anchors every subsequent context
    # section and allows tools to tie suggestions to a specific Jira item.
    story: JiraStory

    # High-level domain or product background (why this work matters). Keeping
    # this separate from the story body lets Copilot reason about business goals.
    business_context: str = Field(..., description="Business and domain context")

    # Linked pull requests represented as lightweight dictionaries. A list of
    # objects gives assistants direct access to structured implementation history.
    related_prs: list[dict] = Field(
        default_factory=list,
        description="Related pull request metadata",
    )

    # Known risk statements gathered during planning. Distinct risk entries make
    # it easier for Copilot to proactively suggest safeguards and test coverage.
    risks: list[str] = Field(default_factory=list, description="Known delivery risks")

    # Unresolved questions that still need product/engineering clarification.
    # Explicitly surfacing these helps an assistant avoid inventing requirements.
    open_questions: list[str] = Field(
        default_factory=list,
        description="Outstanding questions requiring clarification",
    )
