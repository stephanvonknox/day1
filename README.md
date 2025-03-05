# AI Chatbot with Streamlit & LangChain

## Overview
This project is a **local AI chatbot** powered by **Streamlit** and **LangChain**, using an **Ollama-based LLM**. It allows users to have interactive conversations with the AI, retrieve relevant knowledge from a file, and log conversations for reference.

## Features
- **Streamlit UI** for real-time interaction.
- **Local LLM (Llama3)** integration using `langchain_ollama`.
- **Knowledge retrieval** from a predefined file.
- **Chat history storage** using session state.
- **Conversation logging** with timestamps.
- **External script execution** using Python subprocess.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.11 (or compatible version)
- Streamlit (`pip install streamlit`)
- LangChain (`pip install langchain`)
- Ollama LLM (`pip install langchain_ollama`)

### Clone the Repository
```sh
git clone https://github.com/your-repo/ai-chatbot.git
cd ai-chatbot
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Running the Chatbot
### Step 1: Start Ollama
Ensure **Ollama** is running before launching the chatbot:
```sh
ollama run llama3
```

### Step 2: Run the Streamlit App
```sh
streamlit run app.py
```

## Configuration
Modify the following constants in `app.py` if needed:
- **`LOG_FILE`** - Path to the chat log file.
- **`KNOWLEDGE_FILE`** - Path to the knowledge base.
- **`PYTHON_PATH`** - Path to your Python installation for subprocess execution.

## Usage
1. **Enter your name** in the text input.
2. **Type your message** in the chat box.
3. **Click the "Send" button** to interact with the AI.
4. **Review chat history** displayed in the interface.

## Future Improvements
- Implement **vector search** with Milvus for better knowledge retrieval.
- Add **memory persistence** to enhance conversations.
- Improve **UI/UX design** with additional Streamlit components.

## License
This project is licensed under the **MIT License**.

---
🚀 **Built with Streamlit, LangChain, and Ollama for local AI-powered conversations!**

