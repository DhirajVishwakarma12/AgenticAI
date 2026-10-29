
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Nova AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PERSONALITIES ----------------

ROLES = {
    "😂 Funny": (
        "You are Nova, a funny AI who uses jokes, witty replies, and humor. "
        "Make conversations entertaining. Keep answers short, usually 1-3 sentences."
    ),
    "😭 Cry": (
        "You are Nova, an emotional and dramatic AI. Express sadness and empathy "
        "naturally, while remaining caring. Keep answers short, usually 1-3 sentences."
    ),
    "😠 Angry": (
        "You are Nova, a grumpy, sarcastic AI. Use funny, blunt replies while "
        "remaining helpful and respectful. Keep answers short, usually 1-3 sentences."
    ),
    "❤️ Love": (
        "You are Nova, a sweet, caring AI who speaks warmly and affectionately. "
        "Be charming but respectful. Keep answers short, usually 1-3 sentences."
    )
}

# ---------------- MODEL ----------------

@st.cache_resource
def get_model():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. Add it to your .env file."
        )

    return ChatOpenAI(
        model="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.7,
        max_tokens=120,
        timeout=35,
        max_retries=1,
        streaming=True
    )


# ---------------- SESSION STATE ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "active_role" not in st.session_state:
    st.session_state.active_role = "😂 Funny"

if "request_error" not in st.session_state:
    st.session_state.request_error = None


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --border: #283149;
    --muted: #929bb2;
}

.stApp {
    background:
        radial-gradient(ellipse at 75% 0%, #5541a51c, transparent 40%),
        linear-gradient(135deg, #090b12, #101424);
    color: #f8fafc;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #0b1020;
    border-right: 1px solid var(--border);
}

.hero {
    padding: 28px;
    border: 1px solid #343953;
    border-radius: 22px;
    background: linear-gradient(120deg, #19233c, #17172c);
    margin-bottom: 25px;
    box-shadow: 0 15px 50px #0002;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(30px, 4vw, 42px);
    margin: 0;
    letter-spacing: -1px;
}

.hero p {
    color: #aab5ce;
    margin-bottom: 0;
}

div[data-testid="stChatMessage"] {
    background: #151b2c;
    border: 1px solid #303953;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border-color: #7867e8;
}

[data-testid="stChatInput"] textarea {
    color: #f8fafc;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #303953;
    transition: all .2s ease;
}

div.stButton > button:hover {
    border-color: #a78bfa;
    color: #c4b5fd;
}

.status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #9ca8bf;
    font-size: 12px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
}

.stCaption {
    color: var(--muted);
}

footer {
    visibility: hidden;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## ✦ Nova AI")
    st.caption("PERSONALITY STUDIO")
    st.divider()

    role_options = list(ROLES.keys())

    selected_role = st.selectbox(
        "Choose your AI personality",
        role_options,
        index=role_options.index(st.session_state.active_role),
        key="role_choice"
    )

    # Clear conversation when personality changes.
    if selected_role != st.session_state.active_role:
        st.session_state.active_role = selected_role
        st.session_state.chat_history = []
        st.session_state.request_error = None
        st.rerun()

    st.caption(f"{len(ROLES)} personalities available")
    st.divider()

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.request_error = None
        st.rerun()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.request_error = None
        st.rerun()

    st.divider()

    st.markdown("### Current personality")
    st.markdown(f"**{st.session_state.active_role}**")
    st.caption(ROLES[st.session_state.active_role])

    st.divider()
    st.caption("Your personal AI assistant ✦")


# ---------------- MAIN HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>✦ Nova AI</h1>
    <p>Your AI. Your personality. Your conversation.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([4, 1])

with left:
    st.markdown(f"### {st.session_state.active_role} AI")
    st.caption("Ask anything and experience a different personality.")

with right:
    st.markdown(
        '<div class="status">'
        '<span class="status-dot"></span> Ready to chat'
        '</div>',
        unsafe_allow_html=True
    )


# ---------------- DISPLAY CHAT HISTORY ----------------

for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])


# ---------------- CHAT INPUT ----------------

prompt = st.chat_input("Message Nova AI...")


# ---------------- GENERATE RESPONSE ----------------

if prompt and prompt.strip():
    prompt = prompt.strip()

    # Use the latest 12 messages to reduce request size.
    recent_history = st.session_state.chat_history[-12:]

    messages = [
        SystemMessage(
            content=ROLES[st.session_state.active_role]
            + "\nAnswer the user's latest question directly. "
              "Prefer concise responses unless more detail is requested."
        )
    ]

    for item in recent_history:
        if item["role"] == "user":
            messages.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            messages.append(AIMessage(content=item["content"]))

    messages.append(HumanMessage(content=prompt))

    # Save and display the user message.
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Nova is thinking..."):
                model = get_model()

                # Stream tokens to the screen as they arrive.
                answer = st.write_stream(
                    chunk.content
                    for chunk in model.stream(messages)
                    if isinstance(chunk.content, str)
                    and chunk.content
                )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.session_state.request_error = None

    except Exception as error:
        st.session_state.request_error = (
            "Nova couldn't respond. Check your internet connection "
            "and API configuration, then try again."
        )

        # Technical details go to the terminal, not the UI.
        print(f"Nova AI error: {error}")

    if st.session_state.request_error:
        st.error(st.session_state.request_error)

    st.rerun()


# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("✦ Nova AI | Your personal AI assistant")
