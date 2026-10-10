import uuid
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from chat import chatbot,get_all_threads



# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Nexora AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #0b0d14;
    --panel: #11141e;
    --panel-hover: #191d2a;
    --border: rgba(255,255,255,0.085);
    --text: #f0f2fa;
    --muted: #9299b0;
    --accent: #9b8cff;
    --accent-2: #6c7cff;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(11,13,20,0.88);
}

[data-testid="stAppViewContainer"] > .main {
    background:
        radial-gradient(ellipse at 50% 0%,
        rgba(100,90,220,0.09), transparent 48%),
        var(--bg);
}

.block-container {
    max-width: 1120px;
    padding: 2rem 2rem 8rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.7px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0e1019;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.4rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 6px 25px;
}

.brand-icon {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background: linear-gradient(135deg, #a99aff, #6469f6);
    box-shadow: 0 5px 28px rgba(120,105,255,0.25);
    font-size: 23px;
}

.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 23px;
    font-weight: 700;
    color: #f4f3ff;
}

.brand-caption {
    color: #9299b0;
    font-size: 11px;
    margin-top: 2px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.sidebar-label {
    color: #858ba3;
    text-transform: uppercase;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    padding: 14px 5px 8px;
}

/* Buttons */
.stButton > button {
    border: 1px solid var(--border);
    background: #151824;
    color: #e7e8f4;
    border-radius: 12px;
    min-height: 43px;
    transition: all .2s ease;
    font-weight: 500;
}

.stButton > button:hover {
    border-color: rgba(155,140,255,0.65);
    color: #ffffff;
    background: #202239;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
}

/* Main header */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
}

.topbar-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #e5e6f2;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid rgba(100,220,170,0.18);
    border-radius: 50px;
    padding: 7px 12px;
    color: #a2e9c6;
    background: rgba(66,190,130,0.07);
    font-size: 11px;
}

.status-dot {
    width: 7px;
    height: 7px;
    background: #65dba0;
    border-radius: 50%;
    box-shadow: 0 0 10px #65dba0;
}

/* Welcome hero */
.hero {
    text-align: center;
    padding: 44px 10px 30px;
}

.hero-orb {
    width: 76px;
    height: 76px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 25px;
    border: 1px solid rgba(173,160,255,0.3);
    border-radius: 26px;
    background: linear-gradient(145deg,
        rgba(157,137,255,.23),
        rgba(79,92,220,.10));
    box-shadow: 0 0 65px rgba(125,107,255,.12);
    font-size: 35px;
}

.hero h1 {
    font-size: clamp(32px, 4vw, 47px) !important;
    margin: 0 0 12px;
    font-weight: 700;
}

.gradient-text {
    background: linear-gradient(90deg, #c5b9ff, #8294ff, #b4a3ff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 480px;
    margin: 0 auto;
    color: var(--muted);
    line-height: 1.8;
    font-size: 14px;
}

/* Suggestion cards */
.suggestion-title {
    color: #a4a9bd;
    font-size: 11px;
    letter-spacing: 1.7px;
    text-transform: uppercase;
    font-weight: 700;
    margin: 15px 0 13px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg,
        rgba(24,27,43,.94),
        rgba(16,18,29,.94));
    border-color: var(--border);
    border-radius: 18px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(19,22,34,.82);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 20px;
    margin-bottom: 15px;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: rgba(25,25,43,.75);
    border-color: rgba(155,140,255,.13);
}

[data-testid="stChatMessageContent"] {
    color: #e7e9f5;
    line-height: 1.8;
    font-size: 14px;
}

/* Chat input */
[data-testid="stChatInput"] {
    border: 1px solid rgba(155,140,255,.32) !important;
    border-radius: 20px !important;
    background: #151724 !important;
    box-shadow: 0 8px 40px rgba(0,0,0,.22);
}

[data-testid="stChatInput"]:focus-within {
    border-color: #8e81f7 !important;
    box-shadow: 0 0 0 2px rgba(142,129,247,.12);
}

[data-testid="stChatInput"] textarea {
    color: #f2f2fb !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #777f98 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #666d83;
    font-size: 11px;
    padding: 20px 0 0;
}

hr {
    border-color: var(--border) !important;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem 1rem 7rem;
    }

    .hero {
        padding: 28px 4px 20px;
    }

    .hero h1 {
        font-size: 32px !important;
    }

    .topbar {
        margin-bottom: 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# THREAD MANAGEMENT
# =====================================================
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


def message_to_text(message):
    content = message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))

        return "\n".join(parts)

    return ""


def load_thread(thread_id):
    messages = load_conversation(thread_id)
    temp_messages = []

    for message in messages:
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        else:
            continue

        content = message_to_text(message)

        if content:
            temp_messages.append({
                "role": role,
                "content": content
            })

    st.session_state["thread_id"] = thread_id
    st.session_state["messages"] = temp_messages


# =====================================================
# SESSION STATE
# =====================================================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = get_all_threads()

if "pending_prompt" not in st.session_state:
    st.session_state["pending_prompt"] = None

add_thread(st.session_state["thread_id"])


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">✳</div>
        <div>
            <div class="brand-name">Nexora AI</div>
            <div class="brand-caption">Your intelligent companion</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋   New conversation", use_container_width=True):
        reset_chat()
        st.rerun()

    st.markdown(
        '<div class="sidebar-label">Recent conversations</div>',
        unsafe_allow_html=True
    )

    for index, thread_id in enumerate(
        reversed(st.session_state["chat_threads"])
    ):
        if thread_id == st.session_state["thread_id"]:
            icon = "🟣"
        else:
            icon = "💬"

        label = f"{icon}  Conversation {len(st.session_state['chat_threads']) - index}"

        if st.button(
            label,
            key=f"thread_{thread_id}",
            use_container_width=True
        ):
            load_thread(thread_id)
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div style="padding: 8px 4px 16px;">
        <div style="font-size:12px;color:#a5aac0;font-weight:600;">
            ✨ NEXORA INTELLIGENCE
        </div>
        <div style="font-size:11px;color:#777f96;line-height:1.8;margin-top:8px;">
            Ask questions, explore ideas, write code, or solve complex problems.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# MAIN HEADER
# =====================================================
st.markdown("""
<div class="topbar">
    <div class="topbar-title">✳ &nbsp; AI Workspace</div>
    <div class="status-pill">
        <span class="status-dot"></span>
        Assistant ready
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# WELCOME SCREEN
# =====================================================
if not st.session_state["messages"]:

    st.markdown("""
    <div class="hero">
        <div class="hero-orb">✳</div>
        <h1>Meet your next<br><span class="gradient-text">big idea.</span></h1>
        <p>
            Your thoughts, questions, and ambitious projects start here.
            What would you like to explore today?
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="suggestion-title">✦ &nbsp; Try asking me</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### 💻 &nbsp; Coding assistant")
            st.caption("Debug code, learn Python, or build your next project.")

            if st.button(
                "Help me build a project  ↗",
                key="suggest_code",
                use_container_width=True
            ):
                st.session_state["pending_prompt"] = (
                    "Help me plan and build a coding project step by step."
                )
                st.rerun()

        with st.container(border=True):
            st.markdown("#### 🧠 &nbsp; Learn something")
            st.caption("Understand difficult topics with clear explanations.")

            if st.button(
                "Explain a complex topic  ↗",
                key="suggest_learn",
                use_container_width=True
            ):
                st.session_state["pending_prompt"] = (
                    "Teach me a complex topic in a simple, step-by-step way."
                )
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("#### ✍️ &nbsp; Writing studio")
            st.caption("Create content, improve writing, and organize ideas.")

            if st.button(
                "Help me write something  ↗",
                key="suggest_write",
                use_container_width=True
            ):
                st.session_state["pending_prompt"] = (
                    "Help me write a polished piece of content. Ask what I need if necessary."
                )
                st.rerun()

        with st.container(border=True):
            st.markdown("#### 🚀 &nbsp; Brainstorm ideas")
            st.caption("Explore possibilities and find creative solutions.")

            if st.button(
                "Let's brainstorm  ↗",
                key="suggest_ideas",
                use_container_width=True
            ):
                st.session_state["pending_prompt"] = (
                    "Let's brainstorm some creative and useful project ideas."
                )
                st.rerun()


# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================
else:

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# =====================================================
# CHAT INPUT AND RESPONSE
# =====================================================
typed_prompt = st.chat_input("Message Nexora AI...")

user_input = typed_prompt or st.session_state["pending_prompt"]

if user_input:

    st.session_state["pending_prompt"] = None

    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    config = {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }

    with st.chat_message("assistant"):

        try:
            with st.spinner("Nexora is thinking..."):

                def response_stream():
                    for message_chunk, metadata in chatbot.stream(
                        {
                            "messages": [
                                HumanMessage(content=user_input)
                            ]
                        },
                        config=config,
                        stream_mode="messages"
                    ):
                        if not isinstance(message_chunk, AIMessage):
                            continue

                        content = message_chunk.content

                        if isinstance(content, str) and content:
                            yield content

                        elif isinstance(content, list):
                            for item in content:
                                if (
                                    isinstance(item, dict)
                                    and item.get("type") == "text"
                                    and item.get("text")
                                ):
                                    yield item["text"]

                ai_message = st.write_stream(response_stream())

            st.session_state["messages"].append({
                "role": "assistant",
                "content": ai_message
            })

        except Exception as error:
            st.error(f"Something went wrong: {error}")

    st.rerun()


# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div class="footer">
    Powered by Nexora AI &nbsp; · &nbsp; Built for curiosity ✦
</div>
""", unsafe_allow_html=True)