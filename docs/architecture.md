# Architecture

ListOps MCP is a prototype MCP server for email-native LISTSERV moderation assistance.

The prototype is designed to show how an SI agent can use structured MCP tools to help a human moderator process LISTSERV-related messages.

No production email or LISTSERV server is used in this prototype.

---

## Conceptual production flow

```text
LISTSERV moderation notice
        ↓
List owner or moderator mailbox
        ↓
Forward / redirect / direct copy
        ↓
Agency-controlled ListOps intake
        ↓
Local parsing and deterministic safety rules
        ↓
Optional AI classification or summarization
        ↓
Plain-text moderator review card
        ↓
Human moderator decision
        ↓
Validated command preparation
        ↓
Optional LISTSERV command email
        ↓
Audit/event ledger
