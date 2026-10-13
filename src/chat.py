from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage, HumanMessage,SystemMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver  
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode,tools_condition
from tools import search_tool,get_stock_price,calculator
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
    messages: Annotated[list[BaseMessage],add_messages]


# bind tools
tools = [search_tool,get_stock_price,calculator, rag_tool]
model_with_tools = model.bind_tools(tools)


def chat(state : ChatState):

    system_prompt= """
    your are nexora ai , an ai assistant.



    tools instructions :\n
    - if user ask question related to stock , use get_stock_price tool.\n
    - if user ask any complex math question use calculator tool.\n
    - Use "search_tool for current events, recent information, or information
    - Use "rag_tool" for questions about the uploaded PDF or document.\n
    - Always retrieve relevant document content before answering PDF-related questions.\n
    

    "Answer general questions directly when no tool is required. "
    "Do not invent information from the uploaded document. "
    "If the user asks about a PDF but no document is available, ask them to upload a PDF. "
    "After receiving a tool result, provide a clear and helpful final answer."


"""
    
    messages =[
        SystemMessage(content=system_prompt),
        state["messages"]
    ]

    response = model_with_tools.invoke(messages)

    return {"messages":[response]}


tool_node = ToolNode(tools)

con= sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer = SqliteSaver(conn=con)
graph = StateGraph(ChatState)

graph.add_node("chat_node",chat)
graph.add_node("tools",tool_node)
 
graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)

graph.add_edge("tools","chat_node")


chatbot = graph.compile(checkpointer=checkpointer)

def get_all_threads():
    all_threads = set()
    for cpoint in checkpointer.list(None):
        all_threads.add(cpoint.config["configurable"]["thread_id"])

    return list(all_threads)








