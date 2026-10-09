from chat import chatbot
from langchain_core.messages import  HumanMessage

import streamlit as st


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
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:
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

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # LangGraph / chatbot configuration
    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }

    # Get chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_message = st.write_stream(
                message_chunk.content for message_chunk , metadate in chatbot.stream(
                                {
                                    "messages": [
                                        HumanMessage(content=user_input)
                                    ]
                                },
                                config=config,
                                stream_mode="messages"
                            )


            )

            
                

    
        

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message
    })