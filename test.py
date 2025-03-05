import streamlit as st
from langchain_ollama import OllamaLLM
from datetime import datetime
import subprocess

# Streamlit UI setup
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Constants
LOG_FILE = "chat_log.txt"
KNOWLEDGE_FILE = "knowledge.txt"
PYTHON_PATH = "C:/Users/Altair/AppData/Local/Programs/Python/Python311/python.exe"

# Load local AI model with error handling
def load_model():
    """Load the Ollama model with error handling."""
    try:
        return OllamaLLM(model="llama3")  # Ensure Ollama is running
    except Exception as e:
        st.error(f"Error loading AI model: {e}")
        return None

llm = load_model()

def load_knowledge():
    """Load knowledge from file with error handling."""
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.warning("Knowledge file not found. Using empty knowledge base.")
        return ""
    except Exception as e:
        st.error(f"Error loading knowledge file: {e}")
        return ""

def log_conversation(user_name, user_input, ai_response):
    """Log conversation to a file with timestamps and error handling."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {user_name}: {user_input}\n")
            file.write(f"[{timestamp}] AI: {ai_response}\n")
            file.write("-" * 50 + "\n")
    except Exception as e:
        st.error(f"Error logging conversation: {e}")

def retrieve_knowledge(user_input, knowledge_content):
    """Retrieve relevant knowledge snippets from the knowledge base."""
    try:
        return "\n".join(
            [line for line in knowledge_content.split("\n") if any(word in line.lower() for word in user_input.lower().split())]
        ) or ""
    except Exception as e:
        st.error(f"Error retrieving knowledge: {e}")
        return ""

def chat_with_ai(user_input, knowledge_content):
    """Generate AI response based on user input and knowledge base with error handling."""
    if not llm:
        return "AI model unavailable. Please check the model setup."
    
    knowledge_snippet = retrieve_knowledge(user_input, knowledge_content)
    prompt = f"Here is some relevant information:\n{knowledge_snippet}\n\nUser: {user_input}" if knowledge_snippet else user_input
    
    try:
        return llm.invoke(prompt)
    except Exception as e:
        st.error(f"Error generating AI response: {e}")
        return "An error occurred while generating the response."

def run_python_script(script_path):
    """Run an external Python script using a specified Python interpreter."""
    try:
        result = subprocess.run([PYTHON_PATH, script_path], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error executing script: {e}"

# UI Components
st.title("🤖 Local AI Chatbot")
st.markdown("---")

# User Input
user_name = st.text_input("Enter your name:", value="User")
knowledge_content = load_knowledge()

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Interface
st.markdown("## 💬 Chat with AI")
chat_container = st.container()

with chat_container:
    user_input = st.text_area("You:", height=100)
    col1, col2 = st.columns([1, 5])
    with col1:
        send_button = st.button("🚀 Send")
    
    if send_button and user_input:
        response = chat_with_ai(user_input.strip(), knowledge_content)
        if response:
            st.session_state.chat_history.append((user_input, response))
            log_conversation(user_name, user_input, response)
        user_input = ""  # Clear input

# Display Chat History
st.markdown("## 📜 Chat History")
chat_history_container = st.container()

with chat_history_container:
    for user_msg, ai_msg in reversed(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(f"**{user_name}:** {user_msg}")
        with st.chat_message("assistant"):
            st.markdown(f"**AI:** {ai_msg}")

st.markdown("---")
st.caption("🔹 Built with Streamlit & LangChain | AI-powered chatbot")
