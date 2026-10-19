from typing import Annotated

from fastmcp import FastMCP

ALLOWED_DECISIONS = ["APPROVE", "HOLD", "FIX", "ESCALATE"]


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="record_moderator_decision",
        annotations={
            "title": "Record moderator decision",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    async def record_moderator_decision(
        item_id: Annotated[str, "Review item identifier."],
        moderator: Annotated[str, "Moderator email or demo identity."],
        decision: Annotated[str, "APPROVE, HOLD, FIX, or ESCALATE."],
        reason: Annotated[str, "Optional reason for the decision."] = "",
    ) -> dict:
        """Record a simulated human moderation decision.

        This prototype does not send real LISTSERV commands. It returns a
        structured audit-style event for demonstration purposes.
        """
        normalized_decision = decision.upper().strip()

        if normalized_decision not in ALLOWED_DECISIONS:
            return {
                "status": "error",
                "hint": "Decision must be APPROVE, HOLD, FIX, or ESCALATE.",
                "received_decision": decision,
            }

        audit_id = f"AUDIT-{item_id}"

        return {
            "status": "recorded",
            "audit_id": audit_id,
            "item_id": item_id,
            "moderator": moderator,
            "decision": normalized_decision,
            "reason": reason,
            "simulated": True,
            "message": "Moderator decision recorded for demo purposes.",
        }
