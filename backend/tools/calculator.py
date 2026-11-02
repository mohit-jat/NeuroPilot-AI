from langchain_core.tools import tool


@tool
def calculator(a: float, b: float, operation: str) -> str:
    """
    Perform basic mathematical calculations.

    Supported operations:
    add, subtract, multiply, divide
    """

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":

        if b == 0:
            return "Cannot divide by zero."

        result = a / b

    else:
        return "Unsupported operation."

    return str(result)