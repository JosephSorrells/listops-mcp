from typing import Annotated

from fastmcp import FastMCP

SUPPORTED_DECISIONS = ["APPROVE", "HOLD", "FIX", "ESCALATE"]


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="prepare_simulated_listserv_command",
        annotations={
            "title": "Prepare simulated LISTSERV command",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def prepare_simulated_listserv_command(
        item_id: Annotated[str, "Review item identifier."],
        decision: Annotated[str, "APPROVE, HOLD, FIX, or ESCALATE."],
        approval_token_present: Annotated[
            bool,
            "Whether a LISTSERV approval token was detected.",
        ],
    ) -> dict:
        """Prepare a simulated LISTSERV command preview.

        This prototype never sends real LISTSERV commands. It only shows what
        type of action would be prepared after a human moderator decision.
        """
        normalized_decision = decision.upper().strip()

        if normalized_decision not in SUPPORTED_DECISIONS:
            return {
                "status": "error",
                "hint": "Decision must be APPROVE, HOLD, FIX, or ESCALATE.",
                "received_decision": decision,
            }

        if normalized_decision == "APPROVE":
            if not approval_token_present:
                return {
                    "status": "blocked",
                    "item_id": item_id,
                    "simulated": True,
                    "reason": "Cannot prepare approval without an approval token.",
                }

            return {
                "status": "prepared",
                "item_id": item_id,
                "simulated": True,
                "command_type": "APPROVE_POST",
                "command_preview": "OK <redacted-demo-token>",
                "warning": "Demo only. No command was sent to LISTSERV.",
            }

        if normalized_decision == "FIX":
            return {
                "status": "prepared",
                "item_id": item_id,
                "simulated": True,
                "command_type": "REQUEST_REVISION",
                "command_preview": "Send approved revision-request template.",
                "warning": "Demo only. No email was sent.",
            }

        if normalized_decision == "ESCALATE":
            return {
                "status": "prepared",
                "item_id": item_id,
                "simulated": True,
                "command_type": "ESCALATE_FOR_REVIEW",
                "command_preview": "Route item to designated human review queue.",
                "warning": "Demo only. No escalation was sent.",
            }

        return {
            "status": "prepared",
            "item_id": item_id,
            "simulated": True,
            "command_type": "HOLD_POST",
            "command_preview": "Keep item in moderation queue.",
            "warning": "Demo only. No command was sent.",
        }
