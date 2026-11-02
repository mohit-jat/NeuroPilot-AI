
from backend.agents.state import AgentState


async def supervisor_agent(state: AgentState):

    input_type = state["input_type"]

    # Select agent based on input type
    if input_type == "image":

        selected_agent = "vision"

    elif input_type == "audio":

        selected_agent = "audio"

    elif input_type == "document":

        selected_agent = "rag"

    else:

        selected_agent = "text"

    return {
        "selected_agent": selected_agent
    }
