from backend.core.llm import get_llm
from backend.core.prompts import chat_prompt
from backend.core.output_parser import output_parser


# Create LangChain chain
def get_chat_chain():

    llm = get_llm()

    # Check model configuration
    if llm is None:
        return None

    # Connect all components
    chain = chat_prompt | llm | output_parser

    return chain