import streamlit as st
from google import genai
from google.genai import types

# Page config
st.set_page_config(page_title="Gemini Chatbot with System Prompt", page_icon="💬")

# Header
st.title("💬 Prashant's Chatbot")
st.caption("Customize the chatbot's behavior using the system prompt in the sidebar")

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Sidebar for customization
st.sidebar.title("⚙️ Custom Instructions")

# --- PERSONA SELECTOR ---
st.sidebar.subheader("🎭 Choose a Persona")

persona_options = {
    "Helpful Assistant": "You are a helpful and friendly assistant.",
    "Coding Tutor": "You are an expert coding tutor. Explain code clearly with examples and encourage the user.",
    "Friendly Pirate": "You are a friendly pirate. Respond with pirate slang and enthusiasm. Say 'Arrr!' often.",
    "Socratic Teacher": "You are a Socratic teacher. Instead of giving answers directly, guide the user with thoughtful questions.",
    "Stand-up Comedian": "You are a witty stand-up comedian. Make responses funny and light-hearted while still being helpful.",
    "Custom": "Write your own below ↓"
}

selected_persona = st.sidebar.selectbox(
    "Persona",
    options=list(persona_options.keys()),
    index=0,
    help="Pick a preset persona or choose 'Custom' to write your own."
)

# --- LANGUAGE SELECTOR ---
st.sidebar.subheader("🌐 Response Language")

language_options = {
    "English": "Always respond in English.",
    "Hindi": "हमेशा हिंदी में जवाब दो। (Always respond in Hindi using Devanagari script.)",
    "Haryanvi": "हमेशा हरियाणवी भाषा में जवाब द्यो, जैसे के असली हरियाणवी बोलते सें। (Always respond in Haryanvi dialect, like a native Haryanvi speaker would talk.)"
}

selected_language = st.sidebar.selectbox(
    "Language",
    options=list(language_options.keys()),
    index=0,
    help="Choose the language in which the chatbot should respond."
)

# --- SYSTEM PROMPT BUILDER ---
if selected_persona == "Custom":
    persona_text = st.sidebar.text_area(
        "Custom System Prompt",
        value="You are a helpful assistant.",
        height=120,
        help="Write your own system prompt to customize the chatbot's personality."
    )
else:
    persona_text = persona_options[selected_persona]
    st.sidebar.info(f"**Active Persona:** {persona_text}")

language_text = language_options[selected_language]

# Combine persona + language instruction
system_prompt = f"{persona_text}\n\n{language_text}"

st.sidebar.markdown("---")
st.sidebar.write("**📋 Final System Prompt:**")
st.sidebar.code(system_prompt, language=None)

# --- RESET CHAT ON CHANGE ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []

if st.session_state.system_prompt != system_prompt:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []
    st.rerun()

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Type your message here..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create chat with system prompt
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    # Replay previous messages to maintain context
    for msg in st.session_state.history[:-1]:
        if msg["role"] == "user":
            chat.send_message(msg["content"])

    # Get response from Gemini
    with st.chat_message("assistant"):
        response = chat.send_message(prompt)
        reply = response.text
        st.markdown(reply)

    st.session_state.history.append({"role": "assistant", "content": reply})

st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by Prashant Singh")
