from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from tools import search_tool, get_weather, get_stock_price, calculator, purchase_stock
import os
import sqlite3
from langsmith import traceable
from rag import rag_tool


load_dotenv()


def llm():
    return ChatOpenAI(
        api_key=os.getenv("EURON_API_KEY"),
        model="gpt-4o-mini",
        base_url=os.getenv("EURI_BASE_URL"),
        max_completion_tokens=1000
    )


model = llm()


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# bind tools
tools = [search_tool, get_weather, get_stock_price, calculator, rag_tool, purchase_stock]
model_with_tools = model.bind_tools(tools)


SYSTEM_PROMPT = """You are Nexora AI, an AI assistant.

Tool instructions:
- If the user asks a question related to stocks, use the get_stock_price tool.
- If the user asks about current weather, use the get_weather tool. If no city
  is specified, use its default location, Patna.
- If the user asks a complex math question, use the calculator tool.
- Use search_tool for current events and recent information.
- Use rag_tool for questions about the uploaded PDF or document.
- Use purchase_stock for simulating stock purchases.

Answer general questions directly when no tool is required.
Do not invent information from the uploaded document.
If the user asks about a PDF but no document is available, ask them to upload a PDF.
After receiving a tool result, provide a clear and helpful final answer in plain text.
"""


def chat(state: ChatState):

    # FIX: join the lists. Before, state["messages"] was nested inside the list.
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]

    response = model_with_tools.invoke(messages)

    return {"messages": [response]}


tool_node = ToolNode(tools)

con = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=con)
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)

graph.add_edge("tools", "chat_node")


chatbot = graph.compile(checkpointer=checkpointer)


def get_all_threads():
    all_threads = set()
    for cpoint in checkpointer.list(None):
        all_threads.add(cpoint.config["configurable"]["thread_id"])

    return list(all_threads)
