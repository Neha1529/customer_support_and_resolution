"""Complaint resolution helper.

A CrewAI crew of three role-based agents that hand off work in sequence:
investigator -> resolver -> reviewer. Like the FAQ chain, the crew does
its own internal reasoning and just returns one final answer, so it's
exposed to the root agent as a plain function/tool rather than a nested
ADK agent.
"""

from crewai import Agent, Crew, Process, Task

_investigator = CrewAgent(
    role="Complaint investigator",
    goal="Summarise exactly what went wrong for the customer.",
    backstory="You read complaints carefully and extract the concrete facts.",
)
_resolver = CrewAgent(
    role="Complaint resolver",
    goal="Propose a fair resolution based on the investigator's summary.",
    backstory="You propose refunds, replacements, credit or an apology per policy.",
)
_reviewer = CrewAgent(
    role="Policy reviewer",
    goal="Check the proposed resolution against policy before it goes out.",
    backstory="You check resolutions against the refund/shipping policy and rewrite if needed.",
)


def resolve_complaint(complaint_text: str) -> str:
    """Run the complaint-resolution crew on a customer complaint."""
    investigate = Task(
        description=f"Summarise the facts of this complaint:\n{complaint_text}",
        expected_output="A short, factual summary of the complaint.",
        agent=_investigator,
    )
    resolve = Task(
        description="Propose a resolution based on the investigator's summary.",
        expected_output="A proposed resolution with a one-line reason.",
        agent=_resolver,
        context=[investigate],
    )
    review = Task(
        description="Check the proposed resolution against policy and finalise the reply.",
        expected_output="The final, customer-ready reply.",
        agent=_reviewer,
        context=[resolve],
    )
    crew = Crew(
        agents=[_investigator, _resolver, _reviewer],
        tasks=[investigate, resolve, review],
        process=Process.sequential,
    )
    return str(crew.kickoff())
