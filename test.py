import streamlit as st
from langchain_ollama import OllamaLLM
from datetime import datetime

# Streamlit UI setup
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Constants
LOG_FILE = "chat_log.txt"
KNOWLEDGE_FILE = "knowledge.txt"

# Load local AI model with error handling
def load_model():
    """Load the Ollama model with detailed error messages."""
    try:
        llm = OllamaLLM(model="llama3")
        st.success("✅ AI Model Loaded Successfully")
        return llm
    except Exception as e:
        st.error(f"❌ Error loading AI model: {e}")
        import traceback
        st.text(traceback.format_exc())  # Print full error trace
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

def chat_with_ai(user_input, knowledge_content, use_llm_knowledge=False):
    """Generate AI response based on user input and knowledge base with error handling."""
    if not llm:
        return "AI model unavailable. Please check the model setup."

    knowledge_snippet = retrieve_knowledge(user_input, knowledge_content)

    if knowledge_snippet.strip():
        st.info("Using knowledge from file")
        prompt = f"Here is some relevant information:\n{knowledge_snippet}\n\nUser: {user_input}\nAI:"
    elif use_llm_knowledge:
        st.info("Using AI's internal knowledge.")
        prompt = f"Please answer the following question using your internal knowledge:\nUser: {user_input}\nAI:"
    else:
        return None  # Don't generate response yet, wait for button click

    try:
        response = llm.invoke(prompt)
        return response.strip() if response else "AI did not return a response."
    except Exception as e:
        st.error(f"Error generating AI response: {e}")
        return "An error occurred while generating the response."

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
        knowledge_snippet = retrieve_knowledge(user_input.strip(), knowledge_content)

        if knowledge_snippet.strip():
            response = chat_with_ai(user_input.strip(), knowledge_content)
        else:
            st.warning("No relevant knowledge found.")
            st.session_state.show_llm_button = True  # Show LLM button

        if "show_llm_button" in st.session_state and st.session_state.show_llm_button:
            use_llm_button = st.button("💡 Use LLM Knowledge")

            if use_llm_button:
                response = chat_with_ai(user_input.strip(), knowledge_content, use_llm_knowledge=True)
                del st.session_state.show_llm_button  # Hide button after use
        else:
            response = None

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
