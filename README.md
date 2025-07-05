# 🧠 Langroid Chat Example (Local Dev Setup)

This project is a minimal Langroid-based chatbot app that runs locally using Python 3.11. It serves as a sandbox for experimenting with Langroid's ChatAgent + Task abstractions using custom LLM providers like DeepSeek.

---

## ✅ Features

- Simple conversational loop using Langroid's `ChatAgent` and `Task`
- Supports OpenAI and DeepSeek models
- Runs locally with `venv`
- Easily portable to Docker in future

---

## 🛠 Prerequisites

- Python 3.11
- Docker (optional for pulling the official Langroid image)
- DeepSeek or OpenAI API key

---

## 🚀 Steps to Replicate

### 1. Create the project folder
```bash
mkdir langroid-chat
cd langroid-chat
```

### 2. Pull the official Langroid Docker image (optional)
```bash
docker pull langroid/langroid
```

> You won't use the container directly in this setup, but it’s helpful to have as a reference or fallback.

### 3. Create and activate a virtual environment
```bash
python -m venv langroid-venv
.\langroid-venv\Scripts\Activate.ps1
```

### 4. Create a `.env` file with your API key
Create `.env` in the project root:

```env
DEEPSEEK_API_KEY=your-deepseek-key-here
```

> Remove unused keys or placeholder lines from `.env`.

### 5. Install Langroid and extras
```bash
pip install langroid
pip install "langroid[doc-chat,db]"
```

### 6. Create your app
Create a folder `app/` and inside it a file called `chat.py`. Example starter script:

```python
import langroid as lr
from langroid.language_models import OpenAIGPTConfig, Role, LLMMessage

cfg = OpenAIGPTConfig(
    chat_model="deepseek/deepseek-chat"
)

agent = lr.ChatAgent(
    lr.ChatAgentConfig(
        name="HelperBot",
        llm=cfg,
        system_message="You are a helpful assistant."
    )
)

task = lr.Task(agent)
task.run()
```

---

## 🧪 Run Your App

```bash
python app/chat.py
```

---

## 🐳 (Optional) Docker Migration Plan

If you later want to containerize this project:

1. Create a `Dockerfile`
2. Copy in `.env` and your script
3. Use `langroid[doc-chat,db]` in `pip install`
4. Run:  
```bash
docker build -t my-langroid-app .
docker run -it --rm my-langroid-app
```

---

## 📁 Project Structure

```
langroid-chat/
├── app/
│   └── chat.py
├── .env
├── langroid-venv/
├── README.md
```

---

## 📌 Notes

- Langroid supports DeepSeek, OpenAI, OpenRouter, Ollama, and more.
- You can later extend this into a RAG tool, agent debate loop, or Chainlit UI frontend.

---

## 📚 Reference

- [Langroid Docs](https://langroid.github.io/langroid/)
- [Langroid GitHub](https://github.com/langroid/langroid)
