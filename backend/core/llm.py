import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Load environment variables
load_dotenv()


# Read API key
api_key = os.getenv("OPENAI_API_KEY")


# Create LLM model
def get_llm():

    if not api_key or api_key == "YOUR_OPENAI_API_KEY":
        return None

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key
    )

    return llm