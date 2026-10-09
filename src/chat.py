from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
import os


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


checkpointer = MemorySaver()
graph = StateGraph(ChatState)

graph.add_node("chat_node",chat)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot = graph.compile(checkpointer=checkpointer)








