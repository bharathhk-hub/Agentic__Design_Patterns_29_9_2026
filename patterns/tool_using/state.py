from typing import Literal, TypedDict


class AgentState(TypedDict, total=False):
    question: str
    intent: Literal["math", "general"]
    expression: str
    result: str
    response: str


def route_agent(state: AgentState) -> str:
    if state.get("intent") == "math" and state.get("expression"):
        return "math_agent"
    return "fallback_agent"