
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


@tool
def web_search(query: str) -> str:
    """
    Search the internet for information about a topic.
    Use this tool when the user asks for current
    information or information from the web.
    """

    try:

        search = DuckDuckGoSearchRun()

        result = search.run(query)

        return result

    except Exception as error:

        return "Web search error: " + str(error)
