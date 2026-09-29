from functools import lru_cache
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState


class AgentPlan(BaseModel):
    intent: Literal["math", "general"] = Field(
        description="Use math only for a question that can be answered by arithmetic."
    )
    expression: str = Field(
        default="",
        description="A Python-style arithmetic expression for math questions; otherwise empty.",
    )


@lru_cache(maxsize=1)
def _get_models():
    llm = get_llm()
    return llm.with_structured_output(AgentPlan), llm


def reasoning_agent(state: AgentState) -> AgentState:
    try:
        planner, _ = _get_models()
        plan = planner.invoke(
            [
                SystemMessage(
                    content=(
                        "Classify the user's request. Choose math only when it asks for a "
                        "numerical calculation that can be represented by a single arithmetic "
                        "expression. Definitions, explanations, and all other requests are "
                        "general. For math, return only the expression to calculate."
                    )
                ),
                HumanMessage(content=state["question"]),
            ]
        )
    except Exception:
        return {"intent": "general", "expression": ""}

    if isinstance(plan, dict):
        intent = plan.get("intent")
        expression = plan.get("expression", "")
    else:
        intent = plan.intent
        expression = plan.expression

    if intent not in ("math", "general"):
        return {"intent": "general", "expression": ""}

    return {
        "intent": intent,
        "expression": expression.strip() if isinstance(expression, str) else "",
    }


def math_agent(state: AgentState) -> AgentState:
    result = calculator(state.get("expression", ""))
    response = f"The result is {result}." if not result.startswith("Error:") else result
    return {"result": result, "response": response}


def fallback_agent(state: AgentState) -> AgentState:
    _, llm = _get_models()
    answer = llm.invoke(
        [
            SystemMessage(
                content="Answer the user's question clearly and directly. Do not invent calculations."
            ),
            HumanMessage(content=state["question"]),
        ]
    ).content

    if isinstance(answer, list):
        answer = "\n".join(
            block.get("text", "")
            for block in answer
            if isinstance(block, dict) and block.get("type") == "text"
        )

    return {"response": str(answer).strip()}