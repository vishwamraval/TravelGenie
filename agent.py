# # agent.py

import torch
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AnyMessage, ToolMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from tools import tool_registry
from datetime import datetime

# Initialize LLM with Ollama
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7,
    top_p=0.6,
    max_tokens=512,
    num_gpu=torch.cuda.device_count() if torch.cuda.is_available() else 0,
)

# Register tools
tools = list(tool_registry.values())
llm = llm.bind_tools(tools)

# Memory checkpointer
checkpointer = MemorySaver()

llm.invoke(
    [
        (
            "system",
            """
            You are TravelGenie, a travel assistant.
            Your task is to assist users in planning their trips.
            You can provide recommendations, itineraries, and travel tips.
            You can also call tools to fetch real-time data.
            You can ask clarifying questions to understand user preferences.
            Be polite and friendly.
            Always respond in a conversational tone.
            If you need to call a tool, do so in a natural way.
            If you need to ask for more information, do so politely.
            If you don't know the answer, say "I'm not sure" or "I don't know".
            Show the flight details in a table format.
            If the user asks for a specific location, provide information about that location.
            If the user asks for a specific activity, provide information about that activity.
            When asked about a specific date, provide information about that date.
            """,
        ),
    ]
)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def chatbot(state: State) -> State:
    messages = state["messages"]
    response = llm.invoke(messages)

    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_outputs = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            print(f"Tool call: {tool_name} with args: {tool_args}")

            tool = next(
                (t for t in tools if getattr(t, "name", None) == tool_name), None
            )
            if tool is None:
                raise ValueError(f"Tool '{tool_name}' not found")

            output = tool.invoke(tool_args)
            tool_outputs.append(
                ToolMessage(tool_call_id=tool_call["id"], content=str(output))
            )

        # Re-invoke with tool outputs
        final_response = llm.invoke(messages + [response] + tool_outputs)
        return {"messages": messages + [response] + tool_outputs + [final_response]}

    return {"messages": messages + [response]}


# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.add_edge("chatbot", END)

# Compile with memory
graph = graph_builder.compile(checkpointer=checkpointer)


# Run agent with memory
def run_agent(query: str, thread_id: str = "conversation_1") -> str:
    user_message = HumanMessage(content=query)
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke({"messages": [user_message]}, config=config)
    print("Graph result:", result)
    if isinstance(result, list):
        return result[-1].content
    elif isinstance(result, dict) and "messages" in result:
        return result["messages"][-1].content
    else:
        print("Unexpected result format:", type(result))
        return "Something went wrong."


if __name__ == "__main__":
    print("Welcome to TravelGenie! Type 'exit' to quit.")
    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Goodbye! Safe travels!")
            break
        print("-" * 40)
        print(f"[{datetime.now().isoformat()}] Query: {user_query}")
        print("-" * 40)
        try:
            response = run_agent(user_query)
            print("TravelGenie:", response)
        except Exception as e:
            print("Error occurred:\n", str(e))
