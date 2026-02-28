"""Service layer for assembling context bundles."""

from models.context_bundle import ContextBundle
from models.story import JiraStory


class ContextBuilder:
    """Builds context payloads for MCP tools.

    This class centralizes orchestration logic so transport-layer code (MCP tool
    handlers) stays thin. API clients for Jira, GitHub, and other systems will
    be injected here later to replace temporary mocked values.
    """

    def build_bundle(self, jira_key: str) -> ContextBundle:
        """Build a `ContextBundle` for a Jira issue key.

        For now this method returns static, mocked values so the MCP contract is
        stable while external API integrations are still under development.
        """

        story = JiraStory(
            key=jira_key,
            title="Mocked story title",
            description=(
                "Mocked story description used until Jira integration is wired in."
            ),
            deadline=None,
            assignee="unassigned",
        )

        return ContextBundle(
            story=story,
            business_context=(
                "This mocked context represents a feature that improves developer "
                "delivery speed through centralized planning inputs."
            ),
            related_prs=[
                {
                    "number": 101,
                    "title": "Prototype context bundle model",
                    "url": "https://example.com/repo/pull/101",
                    "status": "merged",
                }
            ],
            risks=[
                "Integration APIs are not connected yet, so values may be stale.",
                "Context quality depends on upstream story hygiene.",
            ],
            open_questions=[
                "Should Confluence excerpts be added automatically?",
                "What is the freshness SLA for external sync data?",
            ],
        )
