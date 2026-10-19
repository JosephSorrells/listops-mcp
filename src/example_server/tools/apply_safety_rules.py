from typing import Annotated

from fastmcp import FastMCP

PROCUREMENT_TERMS = [
    "procurement",
    "vendor",
    "solicitation",
    "rfp",
    "rfq",
    "capability statement",
    "contract",
    "proposal",
]

SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
]


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="apply_safety_rules",
        annotations={
            "title": "Apply LISTSERV safety rules",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def apply_safety_rules(
        sender_domain: Annotated[
            str,
            "Sender domain, such as agency.gov or vendor.com.",
        ],
        body_excerpt: Annotated[str, "Message body excerpt."],
        has_attachments: Annotated[
            bool,
            "Whether the message has real attachments.",
        ],
        link_domains: Annotated[
            list[str],
            "Domains extracted from message links.",
        ],
    ) -> dict:
        """Apply deterministic safety rules before any AI recommendation.

        Rules are intentionally conservative. High-risk items should be held
        or escalated for human review.
        """
        flags = []
        rules_triggered = []

        text = (body_excerpt or "").lower()
        sender_domain_l = (sender_domain or "").lower()

        if has_attachments:
            flags.append("ATTACHMENT_PRESENT")
            rules_triggered.append("ATTACHMENT_REQUIRES_FIX_OR_HOLD")

        if any(term in text for term in PROCUREMENT_TERMS):
            flags.append("PROCUREMENT_OR_VENDOR_LANGUAGE")
            rules_triggered.append("PROCUREMENT_LANGUAGE_REQUIRES_ESCALATION")

        if (
            sender_domain_l
            and not sender_domain_l.endswith(".gov")
            and sender_domain_l != "example.gov"
        ):
            flags.append("PRIVATE_SECTOR_OR_EXTERNAL_SENDER")
            rules_triggered.append("EXTERNAL_SENDER_REQUIRES_REVIEW")

        unknown_or_shortened_links = [
            domain
            for domain in link_domains
            if domain in SHORTENERS or not domain.endswith(".gov")
        ]

        if unknown_or_shortened_links:
            flags.append("UNKNOWN_OR_SHORTENED_LINK")
            rules_triggered.append("UNKNOWN_LINK_REQUIRES_REVIEW")

        if "PROCUREMENT_OR_VENDOR_LANGUAGE" in flags:
            recommendation = "ESCALATE"
            risk = "HIGH"
        elif "ATTACHMENT_PRESENT" in flags:
            recommendation = "FIX"
            risk = "MEDIUM"
        elif flags:
            recommendation = "HOLD"
            risk = "MEDIUM"
        else:
            recommendation = "APPROVE"
            risk = "LOW"

        return {
            "risk": risk,
            "recommended_action": recommendation,
            "hard_flags": flags,
            "rules_triggered": rules_triggered,
        }
