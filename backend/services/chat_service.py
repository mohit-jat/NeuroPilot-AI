import os

from backend.agents.graph import agent_graph
from backend.core.database import save_chat, get_chat_history

from langgraph.types import Command


class ChatService:

    async def process_message(
        self,
        message,
        input_type,
        question="",
        thread_id="neuropilot-default"
    ):

        # Get previous chat history for this specific session/thread
        previous_chats = get_chat_history(session_id=thread_id)

        # Keep only last 5 conversations
        previous_chats = previous_chats[-5:]

        chat_history = ""

        for chat in previous_chats:
            chat_history += "User: " + chat["user_message"] + "\n"
            chat_history += "AI: " + chat["ai_response"] + "\n"

        # Run the LangGraph workflow
        result = await agent_graph.ainvoke(
            {
                "message": message,
                "input_type": input_type,
                "response": "",
                "question": question,
                "selected_agent": "",
                "chat_history": chat_history,
                "messages": [],
                "approval_status": "pending"
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        # Check whether human approval is required
        if result.get("__interrupt__"):

            return {
                "success": True,
                "approval_required": True,
                "thread_id": thread_id,
                "response": "Web Search needs your approval."
            }

        ai_response = result["response"]

        # Format user message cleanly for conversation history
        if input_type == "image":
            file_name = os.path.basename(message)
            saved_message = f"{question} [Image: {file_name}]".strip() if question else f"[Image: {file_name}]"
        elif input_type == "audio":
            file_name = os.path.basename(message)
            saved_message = f"[Audio Transcription: {file_name}]"
        elif input_type == "document":
            file_name = os.path.basename(message)
            saved_message = f"{question} [Document: {file_name}]".strip() if question else f"[Document: {file_name}]"
        else:
            saved_message = message

        # Save completed conversation to this specific session
        save_chat(
            saved_message,
            ai_response,
            input_type,
            session_id=thread_id
        )

        return {
            "success": True,
            "approval_required": False,
            "response": ai_response
        }


    async def resume_approval(self, thread_id, decision):

        # Resume the paused workflow
        result = await agent_graph.ainvoke(
            Command(resume=decision),
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        # Check whether another approval is required
        if result.get("__interrupt__"):

            return {
                "success": True,
                "approval_required": True,
                "thread_id": thread_id,
                "response": "Another approval is required."
            }

        ai_response = result["response"]

        # Determine saved message for chat history
        raw_msg = result.get("message", "")
        input_type = result.get("input_type", "text")
        question = result.get("question", "")

        if input_type == "image":
            file_name = os.path.basename(raw_msg)
            saved_message = f"{question} [Image: {file_name}]".strip() if question else f"[Image: {file_name}]"
        elif input_type == "audio":
            file_name = os.path.basename(raw_msg)
            saved_message = f"[Audio Transcription: {file_name}]"
        elif input_type == "document":
            file_name = os.path.basename(raw_msg)
            saved_message = f"{question} [Document: {file_name}]".strip() if question else f"[Document: {file_name}]"
        else:
            saved_message = raw_msg

        # Save the completed conversation to this specific session
        save_chat(
            saved_message,
            ai_response,
            input_type,
            session_id=thread_id
        )

        return {
            "success": True,
            "approval_required": False,
            "response": ai_response
        }
