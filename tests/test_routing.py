import unittest

from patterns.tool_using.state import route_agent


class RoutingTests(unittest.TestCase):
    def test_general_question_uses_fallback(self):
        state = {"question": "Define AI.", "intent": "general"}
        self.assertEqual(route_agent(state), "fallback_agent")

    def test_math_question_uses_tool_when_expression_exists(self):
        state = {
            "question": "What is 2 + 2?",
            "intent": "math",
            "expression": "2 + 2",
        }
        self.assertEqual(route_agent(state), "math_agent")

    def test_incomplete_math_plan_uses_fallback(self):
        state = {"question": "What is 2 + 2?", "intent": "math", "expression": ""}
        self.assertEqual(route_agent(state), "fallback_agent")


if __name__ == "__main__":
    unittest.main()