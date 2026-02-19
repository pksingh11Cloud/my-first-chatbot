import streamlit as st
from google import genai

# Page config
st.set_page_config(page_title="Gemini Chatbot - By Prashant Singh", page_icon="💬")

# Header
st.title("💬 Gemini Chatbot")
st.caption("A simple chatbot powered by Google's Gemini model")

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create chat and replay history
    chat = client.chats.create(model="gemini-2.5-flash")
    for msg in st.session_state.history[:-1]:
        if msg["role"] == "user":
            chat.send_message(msg["content"])

    # Get response from Gemini
    with st.chat_message("assistant"):
        response = chat.send_message(prompt)
        reply = response.text
        st.markdown(reply)

    # Add assistant message to history
    st.session_state.history.append({"role": "assistant", "content": reply})

# Sidebar
st.sidebar.title("About")
st.sidebar.info("This chatbot uses Google's Gemini 2.5 Flash model to have conversations with you.")
st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by [Build Fast with AI](https://buildfastwithai.com)")
