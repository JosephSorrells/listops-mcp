from example_server.tools import (
    apply_safety_rules,
    example_tool,
    generate_review_card,
    parse_listserv_email,
    record_moderator_decision,
)


def register_tools(mcp) -> None:
    example_tool.register(mcp)
    parse_listserv_email.register(mcp)
    apply_safety_rules.register(mcp)
    generate_review_card.register(mcp)
    record_moderator_decision.register(mcp)
