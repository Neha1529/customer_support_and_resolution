""" Order and account helper.

Implemented as a real ADK sub-agent, not a plain function tool, because
answering an order/account question can take more than one step (e.g.
look up the order, then decide whether to also check the account
balance). ADK's own agent gives it that multi-step tool-calling loop for
free; a single Python function wouldn't.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from tools.order_api import get_account_balance, get_order_status

order_agent = Agent(
    name="order_account_agent",
    model="gemini-2.5-flash",
    description=(
        "Handles questions about order status, delivery estimates and "
        "account balance."
    ),
    instruction=(
        "You help customers with order and account questions. Use the "
        "get_order_status tool for delivery/order questions and the "
        "get_account_balance tool for balance questions. If a lookup "
        "returns an error, tell the customer clearly and ask them to "
        "double-check the id."
    ),
    tools=[
        FunctionTool(get_order_status),
        FunctionTool(get_account_balance),
    ],
)