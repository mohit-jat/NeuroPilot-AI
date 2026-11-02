
from datetime import datetime
from langchain_core.tools import tool


@tool
def get_current_datetime() -> str:
    """Get the current date and time."""

    current_time = datetime.now()

    return current_time.strftime(
        "%d-%m-%Y %I:%M:%S %p"
    )
