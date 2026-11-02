from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

from backend.agents.state import AgentState
from backend.agents.supervisor import supervisor_agent

from backend.agents.text_agent import text_agent
from backend.agents.vision_agent import vision_agent
from backend.agents.audio_agent import audio_agent
from backend.agents.rag_agent import rag_agent

from backend.tools.toolkit import tools


# Select the correct agent
def route_agent(state: AgentState):
    return state["selected_agent"]


# Check which tool the AI wants to use
def route_after_text(state: AgentState):

    messages = state.get("messages", [])

    if not messages:
        return END

    last_message = messages[-1]

    if not last_message.tool_calls:
        return END

    # Web Search requires human approval
    for tool_call in last_message.tool_calls:

        if tool_call["name"] == "web_search":
            return "approval"

    # Other tools run directly
    return "tools"


# Ask the human for approval
def approval_node(state: AgentState):

    decision = interrupt({
        "message": "NeuroPilot wants to use Web Search.",
        "tool": "web_search"
    })

    if decision == "approve":

        return {
            "approval_status": "approved"
        }

    return {
        "approval_status": "rejected",
        "response": "Web Search was cancelled by the user."
    }


# Check the human's decision
def route_after_approval(state: AgentState):

    if state.get("approval_status") == "approved":
        return "tools"

    return END


# Create workflow
workflow = StateGraph(AgentState)


# Add nodes
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("text", text_agent)
workflow.add_node("vision", vision_agent)
workflow.add_node("audio", audio_agent)
workflow.add_node("rag", rag_agent)

workflow.add_node("tools", ToolNode(tools))
workflow.add_node("approval", approval_node)


# Starting point
workflow.set_entry_point("supervisor")


# Supervisor routing
workflow.add_conditional_edges(
    "supervisor",
    route_agent,
    {
        "text": "text",
        "vision": "vision",
        "audio": "audio",
        "rag": "rag"
    }
)


# Text agent routing
workflow.add_conditional_edges(
    "text",
    route_after_text,
    {
        "approval": "approval",
        "tools": "tools",
        END: END
    }
)


# Approval routing
workflow.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "tools": "tools",
        END: END
    }
)


# After tool execution, return to Text Agent
workflow.add_edge("tools", "text")


# Other agents finish the workflow
workflow.add_edge("vision", END)
workflow.add_edge("audio", END)
workflow.add_edge("rag", END)


# Save workflow state when approval pauses
memory = MemorySaver()


# Compile workflow
agent_graph = workflow.compile(
    checkpointer=memory
)
