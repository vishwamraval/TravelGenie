# agent.py
import torch
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

# Configure the LLM
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7,
    max_tokens=512,
    num_gpu=torch.cuda.device_count() if torch.cuda.is_available() else 0,
    system_message="""You are a helpful travel assistant. You can help users with travel planning, destination recommendations, and general travel advice.""",
)
llm.verbose = True


def run_agent(query: str) -> str:
    """
    Run the travel agent with the given query.

    Args:
        query (str): The user's query about travel planning.

    Returns:
        str: The agent's response to the query.
    """
    # TODO
    response = llm.invoke([HumanMessage(content=query)])
    return response.content


if __name__ == "__main__":
    test_query = "What is the capital of Texas?"
    print(f"Test query: {test_query}")
    response = run_agent(test_query)
    print(f"Final response: {response}")
