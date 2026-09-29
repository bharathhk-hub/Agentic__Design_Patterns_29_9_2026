import ast
import math
import operator


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_MAX_EXPRESSION_LENGTH = 256
_MAX_POWER = 100
_MAX_INTEGER_BITS = 333
_MAX_FLOAT_MAGNITUDE = 1e100


def _check_number(value):
    if type(value) not in (int, float):
        raise ValueError("Only real numbers are allowed.")
    if type(value) is int and value.bit_length() > _MAX_INTEGER_BITS:
        raise ValueError("Result is too large.")
    if type(value) is float and (
        not math.isfinite(value) or abs(value) > _MAX_FLOAT_MAGNITUDE
    ):
        raise ValueError("Result is too large or not finite.")
    return value


def _evaluate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return _check_number(node.value)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        value = _UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
        return _check_number(value)

    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > _MAX_POWER:
            raise ValueError(f"Exponent must be between -{_MAX_POWER} and {_MAX_POWER}.")
        value = _BINARY_OPERATORS[type(node.op)](left, right)
        return _check_number(value)

    raise ValueError("Only basic arithmetic expressions are allowed.")


def calculator(expression: str) -> str:
    if not expression or len(expression) > _MAX_EXPRESSION_LENGTH:
        return "Error: Expression is empty or too long."

    try:
        tree = ast.parse(expression, mode="eval")
        return str(_evaluate(tree.body))
    except Exception as error:
        return f"Error: {error}"
