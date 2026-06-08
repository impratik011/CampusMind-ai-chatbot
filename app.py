# CampusMind - AI Learning Assistant (Powered by Groq)
# SDG 4: Quality Education

import streamlit as st
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="CampusMind",
    page_icon="🎓",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.main-header {
    text-align: center;
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(90deg, #4F46E5, #06B6D4);
    color: white;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: gray;
    font-size: 12px;
    margin-top: 20px;
}

.chat-container {
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 CampusMind</h1>
    <h4>Your Personal AI Learning Assistant</h4>
    <p>Learn Smarter • Study Better • Ask Anything</p>
</div>
""", unsafe_allow_html=True)

# Get API key from Hugging Face Secret
API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key exists
if not API_KEY:
    st.error("⚠️ GROQ_API_KEY not found. Please add it to Hugging Face Secrets.")
    st.stop()

# Initialize Groq client
try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("📖 About")

    st.write("""
    **CampusMind** is an AI-powered educational assistant
    designed to help students understand concepts,
    solve doubts, and learn more effectively.
    """)

    st.divider()

    st.metric("💬 Messages", len(st.session_state.messages))

    st.divider()

    st.subheader("✨ Features")

    st.markdown("""
    - 📚 Study Assistance
    - 🤖 AI-Powered Responses
    - ⚡ Fast Answers
    - 🎯 Concept Explanations
    - 📝 Learning Support
    """)

    st.divider()

    st.caption("Powered by Groq & Llama 3")

# Welcome message
if len(st.session_state.messages) == 0:
    st.info(
        "👋 Welcome to CampusMind! Ask me anything about programming, mathematics, science, history, technology, or your studies."
    )

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💭 Ask your question here..."):

    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking..."):

            try:
                messages = []

                for m in st.session_state.messages:
                    messages.append(
                        {
                            "role": m["role"],
                            "content": m["content"]
                        }
                    )

                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                )

                reply = chat_completion.choices[0].message.content

                st.markdown(reply)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply
                    }
                )

            except Exception as e:
                st.error(f"Error: {e}")
                st.info(
                    "Try asking a simpler question or verify your API key."
                )

# Footer
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit, Groq API and Llama 3
</div>
""", unsafe_allow_html=True)
