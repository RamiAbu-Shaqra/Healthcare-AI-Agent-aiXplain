import streamlit as st
import json
from agent_manager import get_healthcare_agent

# Use a markdown block with the `unsafe_allow_html=True` flag to inject custom CSS.
hide_streamlit_style = """
<style>
#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Streamlit UI
st.set_page_config(page_title="Agentic AI Chatbot", page_icon="🤖", layout="centered")

robot_icon = "https://cdn-icons-png.flaticon.com/512/4712/4712027.png"
user_icon = "https://cdn-icons-png.flaticon.com/512/847/847969.png"

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Keep track of session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Initialize agent only once
if "agent" not in st.session_state:
    with st.spinner("Setting up the AI agent and tools. Please wait..."):
        st.session_state.agent = get_healthcare_agent()

# Sidebar with new conversation
with st.sidebar:
    st.markdown("<div class='fixed-button-container'>", unsafe_allow_html=True)
    if st.button("New Conversation"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Title
st.markdown("""
    <h2 style='text-align: center; color: #4CAF50;'>🤖 Healthcare AI Agent</h2>
    <p style='text-align: center; color: gray;'>Ask me anything about WHO guidelines or COVID-19 data.</p>
""", unsafe_allow_html=True)

# Input box
user_input = st.chat_input("Type your question here...")

# Show conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar=user_icon):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar=robot_icon):
            st.markdown(msg["content"])

if user_input:
    # Save user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=user_icon):
        st.markdown(user_input)

    # Use a placeholder for the assistant's response to enable the spinner
    with st.chat_message("assistant", avatar=robot_icon):
        placeholder = st.empty()
        with st.spinner("Fetching information ..."):
            # Call the AI agent with user input
            try:
                enhanced_prompt = f"""
                {user_input}

                IMPORTANT: Please provide your response in clear, human-readable text format.
                Do not return JSON, XML, or any structured data format.
                Write your answer as natural language paragraphs that are easy to read and understand.
                """

                response = st.session_state.agent.run(
                    enhanced_prompt,
                    session_id=st.session_state.session_id
                )

                # Get the response
                ai_answer = response.data.output

                # Update session_id if new one was created
                if st.session_state.session_id is None:
                    st.session_state.session_id = response.data.session_id

                # Debug step
                print(json.dumps(response.data["intermediate_steps"], indent=4))

            except Exception as e:
                ai_answer = f"⚠️ Error: {e}"

        placeholder.markdown(ai_answer)

    # Save the assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
    st.rerun()
