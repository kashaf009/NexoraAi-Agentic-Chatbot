from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver  
from langgraph.graph.message import add_messages
import os
import sqlite3
from langsmith import traceable


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



def chat(state : ChatState):

    messages = state["messages"]

    response = model.invoke(messages)

    return {"messages":[response]}

con= sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer = SqliteSaver(conn=con)
graph = StateGraph(ChatState)

graph.add_node("chat_node",chat)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot = graph.compile(checkpointer=checkpointer)

def get_all_threads():
    all_threads = set()
    for cpoint in checkpointer.list(None):
        all_threads.add(cpoint.config["configurable"]["thread_id"])

    return list(all_threads)








