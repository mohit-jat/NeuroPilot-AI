from backend.agents.state import AgentState
from backend.services.rag_service import RAGService


# Create RAG service
rag_service = RAGService()


async def rag_agent(state: AgentState):

    file_path = state["message"]
    question = state["question"]

    # Get answer from document
    answer = await rag_service.ask_document(
        file_path,
        question
    )

    return {
        "response": answer
    }