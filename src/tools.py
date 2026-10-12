from langchain_tavily import TavilySearch
import requests
import os
import math
from dotenv import load_dotenv
import ast
import operator
from langchain_core.tools import tool


load_dotenv()



# Create the search tool

search_tool = TavilySearch(

    max_results=5,
    topic="general",
    search_depth="advanced",

)


# calculator tool

@tool
def calculator(expression: str) -> str:
    """
    Perform basic and advanced mathematical calculations.

    Supports addition, subtraction, multiplication, division,
    powers, square roots, percentages, trigonometry, logarithms,
    factorials, and complex expressions.

    Examples:
        "10 + 20"
        "sqrt(144)"
        "2 ** 10"
        "sin(pi / 2)"
        "log10(1000)"
        "sqrt(144) + (25 / 100) * 800"
    """
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    functions = {
        "sqrt": math.sqrt,
        "abs": abs,
        "round": round,
        "factorial": math.factorial,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "log": math.log,
        "log10": math.log10,
        "log2": math.log2,
        "exp": math.exp,
        "floor": math.floor,
        "ceil": math.ceil,
        "degrees": math.degrees,
        "radians": math.radians,
        "pow": pow,
        "min": min,
        "max": max,
    }

    constants = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
    }

    try:
        if not isinstance(expression, str) or not expression.strip():
            return "Error: Please provide a mathematical expression."

        if len(expression) > 500:
            return "Error: Expression is too long."

        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) not in (int, float):
                    raise ValueError("Only numbers are allowed.")
                return node.value

            if isinstance(node, ast.Name):
                if node.id in constants:
                    return constants[node.id]
                raise ValueError(f"Unknown constant: {node.id}")

            if isinstance(node, ast.BinOp):
                op_type = type(node.op)

                if op_type not in operators:
                    raise ValueError("Unsupported operator.")

                left = evaluate(node.left)
                right = evaluate(node.right)

                if op_type is ast.Pow and abs(right) > 1000:
                    raise ValueError("Exponent is too large.")

                result = operators[op_type](left, right)

                if isinstance(result, complex):
                    raise ValueError("Complex results are not supported.")

                if isinstance(result, (int, float)):
                    if not math.isfinite(result) or abs(result) > 1e100:
                        raise ValueError("Result is too large or undefined.")

                return result

            if isinstance(node, ast.UnaryOp):
                op_type = type(node.op)

                if op_type not in operators:
                    raise ValueError("Unsupported unary operator.")

                return operators[op_type](evaluate(node.operand))

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Unsupported function call.")

                name = node.func.id

                if name not in functions:
                    raise ValueError(f"Unsupported function: {name}")

                if node.keywords:
                    raise ValueError("Keyword arguments are not supported.")

                args = [evaluate(arg) for arg in node.args]
                result = functions[name](*args)

                if isinstance(result, (int, float)):
                    if not math.isfinite(result) or abs(result) > 1e100:
                        raise ValueError("Result is too large or undefined.")

                return result

            raise ValueError("Invalid mathematical expression.")

        result = evaluate(tree)
        return f"Result: {result}"

    except (ValueError, TypeError, SyntaxError, ZeroDivisionError,
            OverflowError) as error:
        return f"Calculation error: {error}"




# stock tool 

@tool

def get_stock_price(symbol: str) -> dict:

    """

    Get the latest available stock price and trading information

    for a company using its stock ticker symbol.

    Examples:

        AAPL = Apple

        MSFT = Microsoft

        IBM = IBM

        RELIANCE.BSE = Reliance Industries on BSE, if supported.

    Args:

        symbol: Stock ticker symbol, such as AAPL or IBM.

    """

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:

        return {"error": "ALPHA_VANTAGE_API_KEY is missing from .env"}

    try:

        response = requests.get(

            "https://www.alphavantage.co/query",

            params={

                "function": "GLOBAL_QUOTE",

                "symbol": symbol.strip().upper(),

                "apikey": api_key,

            },

            timeout=15,

        )

        response.raise_for_status()

        data = response.json()

        # Handle API errors and rate limits

        if "Error Message" in data:

            return {"error": data["Error Message"]}

        if "Note" in data or "Information" in data:

            return {

                "error": data.get("Note") or data.get("Information")

            }

        quote = data.get("Global Quote", {})

        if not quote or not quote.get("05. price"):

            return {

                "error": (

                    f"No stock quote found for '{symbol}'. "

                    "Check the ticker symbol or API availability."

                )

            }

        return {

            "symbol": quote.get("01. symbol"),

            "price": float(quote["05. price"]),

            "latest_trading_day": quote.get("07. latest trading day"),

            "previous_close": quote.get("08. previous close"),

            "change": quote.get("09. change"),

            "change_percent": quote.get("10. change percent"),

            "volume": quote.get("06. volume"),

            "source": "Alpha Vantage",

        }

    except requests.RequestException as e:

        return {"error": f"Failed to fetch stock price: {str(e)}"}

    except (ValueError, TypeError) as e:

        return {"error": f"Invalid API response: {str(e)}"}
    