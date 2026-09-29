import unittest
from types import SimpleNamespace
from unittest.mock import patch

from patterns.tool_using.graph import build_graph


class FakePlanner:
    def invoke(self, messages):
        question = messages[-1].content
        if question == "Define AI.":
            return {"intent": "general", "expression": ""}
        return {"intent": "math", "expression": "((10 + 5) / 2) ** 2"}


class FakeLLM:
    def invoke(self, messages):
        return SimpleNamespace(content="AI is the field of building intelligent systems.")


class GraphTests(unittest.TestCase):
    def run_question(self, question):
        with patch(
            "patterns.tool_using.nodes._get_models",
            return_value=(FakePlanner(), FakeLLM()),
        ):
            return build_graph().invoke({"question": question})

    def test_general_question_uses_fallback_node(self):
        result = self.run_question("Define AI.")
        self.assertEqual(result["response"], "AI is the field of building intelligent systems.")
        self.assertNotIn("result", result)

    def test_arithmetic_question_uses_math_node(self):
        result = self.run_question("What is the square of the average of 10 and 5?")
        self.assertEqual(result["result"], "56.25")
        self.assertEqual(result["response"], "The result is 56.25.")


if __name__ == "__main__":
    unittest.main()