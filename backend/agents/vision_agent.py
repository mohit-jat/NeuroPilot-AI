from backend.agents.state import AgentState
from backend.services.vision_service import VisionService


vision_service = VisionService()


async def vision_agent(state: AgentState):

    image_path = state["message"]

    question = state.get("question", "")

    if not question:
        question = "Describe this image."

    answer = vision_service.understand_image(
        image_path,
        question
    )

    return {
        "response": answer
    }