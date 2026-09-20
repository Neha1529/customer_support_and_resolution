from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An orchestrator which routes user questions to the appropriate agents for processing.',
    instruction=(
        "You are the front door for customer support. For general "
        "questions about policy, shipping or refunds, use the "
        "answer_faq_question tool. For anything about a specific order "
        "or account, delegate to the order_account_agent. For "
        "complaints or dissatisfaction, use the resolve_complaint tool. "
        "Always return the helper's answer to the customer in a clear, "
        "direct way and don't just repeat raw tool output."
    ),
    tools=[
        FunctionTool(answer_faq_question),
        FunctionTool(resolve_complaint),
    ],
    sub_agents=[order_agent],
)

