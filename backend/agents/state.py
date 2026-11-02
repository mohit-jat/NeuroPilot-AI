from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage


class AgentState(TypedDict):

    message: str
    input_type: str
    response: str
    question: str
    selected_agent: str
    chat_history: str

    messages: Annotated[list[AnyMessage], add_messages]
    approval_status: str
