# 🤖 Nexora AI

**Nexora AI** is an intelligent agentic AI chatbot built with Python, Streamlit, LangChain, and LangGraph. It features short-term and long-term memory, Human-in-the-Loop (HITL) functionality, and persistent storage to deliver contextual, interactive, and personalized conversations.

## ✨ Features

- 🧠 **Short-Term Memory** — Maintains context throughout conversations.
- 💾 **Long-Term Memory** — Retains relevant information across conversations.
- 🔄 **Agentic Workflow** — Orchestrates stateful AI workflows using LangGraph.
- 👤 **Human-in-the-Loop (HITL)** — Enables human intervention and approval at configured decision points.
- 🗄️ **Persistent Storage** — Uses SQLite for data persistence.
- 📊 **LLM Observability** — Uses LangSmith for tracing, debugging, and monitoring.
- 💬 **Interactive UI** — Provides a clean chatbot interface powered by Streamlit.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| LangChain | LLM integration and application development |
| LangGraph | Agent orchestration and workflow management |
| LangSmith | Tracing, debugging, and monitoring |
| SQLite | Persistent data storage |

## 🧠 Key Highlights

- 🧠 Context-aware conversations using short-term memory.
- 💾 Persistent personalization through long-term memory.
- 🔄 Stateful agent execution and workflow orchestration.
- 👤 Human oversight through Human-in-the-Loop (HITL) functionality.
- 📊 AI workflow tracing and debugging with LangSmith.


# 🚀 Getting Started

Follow these steps to set up and run Nexora AI locally.

## 1. Clone the Repository

    git clone https://github.com/kashaf009/NexoraAi-Agentic-Chatbot.git
    cd YOUR_REPOSITORY

## 2. Create a Virtual Environment

    python -m venv venv

Activate the virtual environment:

**Windows**
    
    venv\Scripts\activate

**macOS / Linux**

    source venv/bin/activate

## 3. Install Dependencies

    pip install -r requirements.txt

## 4. Configure Environment Variables

Create a `.env` file in the root directory and add your required API keys.

    MODEL_API_KEY=your_model_api_key
    LANGSMITH_TRACING=true
    LANGSMITH_API_KEY=your_langsmith_api_key
    LANGSMITH_PROJECT=nexora-ai

>

## 5. Run the Application

    streamlit run app.py

Open the local URL displayed in your terminal to start interacting with Nexora AI.

> **Note:** Replace `app.py` with your actual Streamlit entry-point filename if necessary.

---

# 🧠 Key Highlights

- 🧠 **Short-Term Memory** — Maintains context throughout conversations.
- 💾 **Long-Term Memory** — Supports personalized interactions across conversations.
- 🔄 **Agentic Workflow** — Orchestrates stateful AI workflows using LangGraph.
- 👤 **Human-in-the-Loop (HITL)** — Enables human intervention and approval at configured decision points.
- 📊 **AI Observability** — Uses LangSmith for tracing, debugging, and monitoring.
- 🗄️ **Persistent Storage** — Uses SQLite for data persistence.

---

# 👨‍💻 Author

**Kashaf Khan**

- GitHub: [@kashaf009](https://github.com/kashaf009)
