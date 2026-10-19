# Safety Model

This prototype is a human-in-the-loop LISTSERV moderation assistant.

## Prototype boundaries

This prototype:

- Uses synthetic sample messages only.
- Does not connect to a production LISTSERV server.
- Does not read a production mailbox.
- Does not send real emails.
- Does not send real LISTSERV commands.
- Does not make autonomous moderation decisions.

## Design principles

- Rules run before AI summaries.
- Attachments, unknown links, private-sector vendor language, and sensitive-topic indicators are routed to HOLD, FIX, or ESCALATE.
- Moderator review cards use plain text and one-word replies.
- Command generation is simulated.
- Production use would require agency approval, mailbox authorization, privacy review, records review, security assessment, and controlled command execution.

## High-risk cases

The prototype is designed to flag or escalate:

- Attachments.
- Unknown external links.
- Shortened links.
- Private-sector sender domains.
- Vendor or procurement language.
- Possible sensitive-topic messages.
- Ambiguous messages.

## Safety principle

The system may recommend, summarize, and route. Humans remain responsible for consequential moderation decisions.
