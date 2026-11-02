from backend.agents.state import AgentState
from backend.services.audio_service import AudioService


audio_service = AudioService()


async def audio_agent(state: AgentState):

    audio_path = state["message"]

    transcript = audio_service.transcribe_audio(
        audio_path
    )

    return {
        "response": transcript
    }