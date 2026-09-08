import ast
import math
import operator


def calculate(expression: str):
    """
    Calculator an toàn.

    Hỗ trợ:
    +  -  *  /  //  %  **
    ()
    abs(), round()
    sqrt(), sin(), cos(), tan()
    log(), log10()
    min(), max()
    pi, e

    Ví dụ:
        calculator("(15 + 5) * 3")
        calculator("sqrt(144) + 2**3")
        calculator("round(10 / 3, 2)")
    """

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    functions = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
    }

    constants = {
        "pi": math.pi,
        "e": math.e,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Chỉ hỗ trợ số")

        if isinstance(node, ast.BinOp):
            op = operators.get(type(node.op))

            if op is None:
                raise ValueError("Phép toán không được hỗ trợ")

            left = evaluate(node.left)
            right = evaluate(node.right)

            return op(left, right)

        if isinstance(node, ast.UnaryOp):
            op = operators.get(type(node.op))

            if op is None:
                raise ValueError("Phép toán không được hỗ trợ")

            return op(evaluate(node.operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Hàm không hợp lệ")

            func_name = node.func.id
            func = functions.get(func_name)

            if func is None:
                raise ValueError(f"Hàm '{func_name}' không được hỗ trợ")

            args = [evaluate(arg) for arg in node.args]

            return func(*args)

        if isinstance(node, ast.Name):
            if node.id in constants:
                return constants[node.id]

            raise ValueError(f"Biến '{node.id}' không tồn tại")

        raise ValueError("Biểu thức không hợp lệ")

    try:
        tree = ast.parse(expression, mode="eval")
        return f"{evaluate(tree)}"

    except ZeroDivisionError:
        return "Error: Division by zero"

    except Exception as e:
        return f"Error: {e}"