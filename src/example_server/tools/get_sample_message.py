from typing import Annotated

from fastmcp import FastMCP

LOW_RISK_ANNOUNCEMENT = """From: LISTSERV@listserv.example.gov
To: owner-fedwg@example.gov
Subject: FED-WG message approval required

LISTSERV has received a message for FED-WG that requires approval.

Original sender:
jane.doe@example.gov

Original subject:
[ANNOUNCEMENT] October working group meeting

Message body:
Please distribute the following meeting announcement.
The October working group meeting will be held next Thursday.
Details are available at https://agency.gov/meeting.

Approval token:
OK DEMO-TOKEN-001
"""

ATTACHMENT_ISSUE = """From: LISTSERV@listserv.example.gov
To: owner-fedwg@example.gov
Subject: FED-WG message approval required

LISTSERV has received a message for FED-WG that requires approval.

Original sender:
pat.smith@example.gov

Original subject:
[ACTION REQUESTED] Review attached agenda

Message body:
Please see attached agenda and distribute to the group.

Attachment:
agenda.xlsx

Approval token:
OK DEMO-TOKEN-002
"""

PRIVATE_SECTOR_VENDOR = """From: LISTSERV@listserv.example.gov
To: owner-fedwg@example.gov
Subject: FED-WG message approval required

LISTSERV has received a message for FED-WG that requires approval.

Original sender:
alex@vendor-example.com

Original subject:
Capability statement for upcoming procurement

Message body:
Our company would like to share our capability statement.
They would also like to discuss potential support for an upcoming solicitation.
Please see attached.

Attachment:
capability-statement.pdf

Approval token:
OK DEMO-TOKEN-003
"""

SAMPLE_MESSAGES = {
    "attachment_issue": ATTACHMENT_ISSUE,
    "low_risk_announcement": LOW_RISK_ANNOUNCEMENT,
    "private_sector_vendor": PRIVATE_SECTOR_VENDOR,
}


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="get_sample_message",
        annotations={
            "title": "Get sample LISTSERV message",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def get_sample_message(
        sample_name: Annotated[
            str,
            "Sample name for the synthetic LISTSERV message.",
        ],
    ) -> dict:
        """Return a synthetic LISTSERV-like sample message for demos.

        This tool only returns synthetic data and does not access a mailbox.
        """
        if sample_name not in SAMPLE_MESSAGES:
            return {
                "status": "error",
                "hint": "Use one of the available sample message names.",
                "available_samples": sorted(SAMPLE_MESSAGES.keys()),
            }

        return {
            "status": "ok",
            "sample_name": sample_name,
            "raw_email": SAMPLE_MESSAGES[sample_name],
        }
