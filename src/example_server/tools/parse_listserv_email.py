from typing import Annotated
import re
from fastmcp import FastMCP


def _find_line_value(text: str, label: str) -> str | None:
    pattern = rf"^{re.escape(label)}:\s*(.+)$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else None


def _extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s<>\"]+", text or "")


def _domain_from_url(url: str) -> str:
    without_scheme = re.sub(r"^https?://", "", url)
    return without_scheme.split("/")[0].lower()


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="parse_listserv_email",
        annotations={
            "title": "Parse LISTSERV email",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def parse_listserv_email(
        raw_email: Annotated[str, "Raw or synthetic LISTSERV email text."]
    ) -> dict:
        """Parse a LISTSERV-like moderation email into structured fields.

        This demo tool uses synthetic or forwarded LISTSERV-like text.
        It does not connect to a production LISTSERV server.
        """
        subject = _find_line_value(raw_email, "Subject")
        original_sender = _find_line_value(raw_email, "Original sender")
        original_subject = _find_line_value(raw_email, "Original subject")

        token_match = re.search(r"\bOK\s+[A-Z0-9\-]+", raw_email, flags=re.IGNORECASE)
        approval_token = token_match.group(0) if token_match else None

        list_match = re.search(r"message for\s+([A-Z0-9\-_]+)", raw_email, flags=re.IGNORECASE)
        list_name = list_match.group(1).upper() if list_match else "UNKNOWN"

        urls = _extract_urls(raw_email)
        link_domains = sorted({_domain_from_url(url) for url in urls})

        attachment_names = []
        attachment_match = re.search(
            r"^Attachment:\s*(.+)$",
            raw_email,
            flags=re.MULTILINE | re.IGNORECASE,
        )
        if attachment_match:
            attachment_names.append(attachment_match.group(1).strip())

        body_match = re.search(
            r"Message body:\s*(.+?)(?:\n\n|\Z)",
            raw_email,
            flags=re.DOTALL | re.IGNORECASE,
        )
        body_excerpt = body_match.group(1).strip()[:500] if body_match else raw_email[:500]

        sender_domain = "unknown"
        if original_sender and "@" in original_sender:
            sender_domain = original_sender.split("@")[-1].lower()

        return {
            "item_id": "DEMO-ITEM-001",
            "list_name": list_name,
            "message_type": "moderation_request",
            "sender": original_sender or "unknown",
            "sender_domain": sender_domain,
            "subject": original_subject or subject or "",
            "body_excerpt": body_excerpt,
            "has_attachments": len(attachment_names) > 0,
            "attachment_names": attachment_names,
            "links": urls,
            "link_domains": link_domains,
            "approval_token_present": approval_token is not None,
            "approval_token_redacted": "OK <redacted>" if approval_token else None,
        }
