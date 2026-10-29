
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(
    page_title="Nova AI",
    page_icon="✦",
    layout="centered"
)

# Three personalities
ROLES = {
    "Angry": "You are an angry, grumpy AI who uses funny sarcasm but still helps the user. Keep replies short.",
    "Funny": "You are a funny AI who uses jokes, witty replies, and humor. Keep replies short.",
    "Genius": "You are a genius AI who gives logical, intelligent, and accurate answers. Keep replies concise."
}

# AI model
model = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3,
    max_tokens=150,
    timeout=35,
    max_retries=1,
    streaming=True
)

# Conversation state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Funny"

# Minimal chat styling
st.markdown("""
<style>
.stApp {
    background: #0b0d14;
    color: #f5f5f5;
}

.block-container {
    max-width: 800px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

[data-testid="stChatMessage"] {
    background: #141722;
    border: 1px solid #272c3c;
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #393f56;
    border-radius: 14px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Chat title
st.title("✦ Nova AI")

# Personality selection
selected_role = st.selectbox(
    "Personality",
    list(ROLES.keys()),
    index=list(ROLES.keys()).index(st.session_state.selected_role)
)

if selected_role != st.session_state.selected_role:
    st.session_state.selected_role = selected_role
    st.session_state.messages = []
    st.rerun()

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Message input
prompt = st.chat_input("Message Nova AI...")

if prompt and prompt.strip():
    prompt = prompt.strip()

    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = [
        SystemMessage(content=ROLES[st.session_state.selected_role])
    ]

    for message in st.session_state.messages[-12:]:
        if message["role"] == "user":
            conversation.append(HumanMessage(content=message["content"]))
        else:
            conversation.append(AIMessage(content=message["content"]))

    conversation.append(HumanMessage(content=prompt))

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        with st.chat_message("assistant"):
            answer = st.write_stream(
                chunk.content
                for chunk in model.stream(conversation)
                if isinstance(chunk.content, str) and chunk.content
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as error:
        st.error("Unable to get a response. Please try again.")
        print(f"Nova AI error: {error}")

    st.rerun()
