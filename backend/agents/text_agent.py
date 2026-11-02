
from backend.agents.state import AgentState
from backend.core.llm import get_llm
from backend.core.prompts import chat_prompt

from backend.tools.toolkit import tools


async def text_agent(state: AgentState):

    llm = get_llm()

    if llm is None:
        return {
            "response": "OpenAI API key is pending. Please configure it in .env."
        }

    try:

        # Connect tools with LLM
        llm_with_tools = llm.bind_tools(tools)

        # Prepare prompt
        messages = chat_prompt.format_messages(
            user_message=state["message"],
            chat_history=state.get("chat_history", "")
        )

        # Add previous tool messages
        messages.extend(state.get("messages", []))

        # Get AI response
        response = await llm_with_tools.ainvoke(messages)

        return {
            "messages": [response],
            "response": response.content
        }

    except Exception as error:

        return {
            "response": "AI model error: " + str(error)
        }
