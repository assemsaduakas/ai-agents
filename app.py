import streamlit as st
from agents.orchestrator import AgentOrchestrator
from agents.memory import ConversationMemory

st.set_page_config(page_title="Weather & News Agent", layout="centered")

st.title("🌍 Weather & News Assistant")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "agent" not in st.session_state:
    st.session_state.agent = AgentOrchestrator(st.session_state.memory)

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask me about weather or news:")

if st.button("Send") and user_input:
    answer = st.session_state.agent.handle_query(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Assistant", answer))

for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:** {message}")