from typing import Annotated
from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="generate_review_card",
        annotations={
            "title": "Generate accessible moderator review card",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def generate_review_card(
        subject: Annotated[str, "Original message subject."],
        sender: Annotated[str, "Original sender email."],
        summary: Annotated[str, "Plain-language message summary."],
        risk: Annotated[str, "LOW, MEDIUM, or HIGH."],
        recommended_action: Annotated[str, "APPROVE, HOLD, FIX, or ESCALATE."],
        reasons: Annotated[list[str], "Reasons for the recommendation."],
    ) -> dict:
        """Generate a plain-text, accessible review card for email moderators.

        The card is designed for email clients, screen readers, mobile users,
        and moderators who should only need one-word replies.
        """
        reasons_text = "\n".join(f"- {reason}" for reason in reasons) if reasons else "- No reasons provided."

        card = f"""ACTION NEEDED

A message is waiting for review.

Recommended action:
{recommended_action}

What happens if you approve:
The message will be sent to the list.

To approve:
Reply APPROVE.

Other choices:
Reply HOLD to keep it from sending.
Reply FIX to ask the sender to revise.
Reply ESCALATE to send it for special review.

Risk:
{risk}

Why:
{reasons_text}

Message summary:
{summary}

Sender:
{sender}

Subject:
{subject}

If you need help:
Reply HELP.

End of action section.
"""

        return {
            "review_card": card,
            "recommended_action": recommended_action,
            "risk": risk,
        }
