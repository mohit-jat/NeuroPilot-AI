import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class AudioService:

    def transcribe_audio(self, file_path):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or api_key == "YOUR_OPENAI_API_KEY":
            return "OpenAI API key is pending."

        try:

            client = OpenAI(api_key=api_key)

            with open(file_path, "rb") as audio_file:

                result = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

            return result.text

        except Exception as error:

            return "Audio transcription error: " + str(error)