from example_server.tools import (
    example_tool,
    parse_listserv_email,
    apply_safety_rules,
    generate_review_card,
)


def register_tools(mcp) -> None:
    example_tool.register(mcp)
    parse_listserv_email.register(mcp)
    apply_safety_rules.register(mcp)
    generate_review_card.register(mcp)
