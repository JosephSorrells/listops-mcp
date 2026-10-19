# ListOps MCP Demo Script

## Demo goal

Show how a federal LISTSERV moderator could use an SI agent and MCP tools to review LISTSERV messages without changing the underlying L-Soft server.

The demo uses synthetic data only. No real email is read and no real LISTSERV commands are sent.

---

## Scenario 1: Low-risk announcement

### User prompt

Review the `low_risk_announcement` sample message.

### Expected tool flow

1. `get_sample_message`
2. `parse_listserv_email`
3. `apply_safety_rules`
4. `generate_review_card`

### Expected result

The message is a routine federal working group meeting announcement.

Recommended action:

`APPROVE`

Reason:

- Federal sender.
- No attachments.
- Approved `.gov` link.

---

## Scenario 2: Attachment issue

### User prompt

Review the `attachment_issue` sample message.

### Expected tool flow

1. `get_sample_message`
2. `parse_listserv_email`
3. `apply_safety_rules`
4. `generate_review_card`

### Expected result

The message asks recipients to review an attachment.

Recommended action:

`FIX`

Reason:

- Real attachment detected.
- Message says "see attached."
- List policy should discourage distributing attachments.

---

## Scenario 3: Private-sector vendor/procurement message

### User prompt

Review the `private_sector_vendor` sample message.

### Expected tool flow

1. `get_sample_message`
2. `parse_listserv_email`
3. `apply_safety_rules`
4. `generate_review_card`

### Expected result

The message comes from a private-sector sender and includes vendor/procurement language.

Recommended action:

`ESCALATE`

Reason:

- Private-sector sender.
- Vendor/procurement language.
- Attachment present.
- Human review required.

---

## Scenario 4: Simulated moderator decision

### User prompt

Record a moderator decision of ESCALATE for the private-sector vendor item.

### Expected tool flow

1. `record_moderator_decision`
2. `prepare_simulated_listserv_command`

### Expected result

The decision is recorded in a simulated audit event.

No real LISTSERV command is sent.

The command preparation tool returns a simulated command preview only.

---

## Safety message to emphasize

ListOps MCP does not replace LISTSERV. It wraps legacy LISTSERV workflows with a safe, email-native, human-in-the-loop moderation assistant.

The prototype:

- Uses synthetic data.
- Does not access real mailboxes.
- Does not send real emails.
- Does not send real LISTSERV commands.
- Keeps humans responsible for consequential decisions.

---

## 30-second pitch

Federal LISTSERVs remain important collaboration channels, but moderation often happens manually in individual inboxes. ListOps MCP gives an SI agent safe tools to parse LISTSERV-like messages, apply deterministic safety rules, generate accessible moderator review cards, and record simulated human decisions. It is system-agnostic, email-native, and designed to work without changing the underlying L-Soft server.
