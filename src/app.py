from chat import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid
import streamlit as st


# -----------------------------
# Thread ID functions
# -----------------------------
def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    st.session_state["thread_id"] = generate_thread_id()
    st.session_state["messages"] = []
    add_thread(st.session_state["thread_id"])


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Nexora AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Nexora AI")
st.caption("Your Agentic AI Assistant")


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

# Register the initial conversation
add_thread(st.session_state["thread_id"])


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Conversations")

if st.sidebar.button("➕ New Chat"):
    reset_chat()
    st.rerun()


# -----------------------------
# Conversation history
# -----------------------------
for thread_id in reversed(st.session_state["chat_threads"]):

    if st.sidebar.button(
        f"💬 Chat {st.session_state['chat_threads'].index(thread_id) + 1}",
        key=thread_id
    ):
        st.session_state["thread_id"] = thread_id

        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):
                role = "user"

            elif isinstance(message, AIMessage):
                role = "assistant"

            else:
                continue

            # Only display text messages
            if isinstance(message.content, str):
                content = message.content

            elif isinstance(message.content, list):
                content = "\n".join(
                    item["text"]
                    for item in message.content
                    if isinstance(item, dict)
                    and item.get("type") == "text"
                    and isinstance(item.get("text"), str)
                )

            else:
                continue

            temp_messages.append({
                "role": role,
                "content": content
            })

        st.session_state["messages"] = temp_messages

        st.rerun()


# -----------------------------
# Display current conversation
# -----------------------------
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat input
# -----------------------------
user_input = st.chat_input("Ask Nexora AI anything...")


if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })

    # LangGraph configuration
    config = {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }

    # Stream chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            ai_message = st.write_stream(
                message_chunk.content
                for message_chunk, metadata in chatbot.stream(
                    {
                        "messages": [
                            HumanMessage(content=user_input)
                        ]
                    },
                    config=config,
                    stream_mode="messages"
                )
                if isinstance(message_chunk, AIMessage)
                and isinstance(message_chunk.content, str)
                and message_chunk.content
            )

    # Save assistant response
    st.session_state["messages"].append({
        "role": "assistant",
        "content": ai_message
    })