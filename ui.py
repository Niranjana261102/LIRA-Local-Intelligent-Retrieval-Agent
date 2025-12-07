import streamlit as st
import requests
import json

# --- CONFIGURATION ---
API_URL = "http://localhost:8000"
st.set_page_config(
    page_title="LIRA | Intelligent Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM AESTHETIC CSS ---
st.markdown("""
<style>
    /* 1. BACKGROUND: Soft Animated Gradient */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Helvetica Neue', sans-serif;
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* 2. SIDEBAR: Glassmorphism Effect */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.85); /* Semi-transparent white */
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.3);
    }

    /* 3. HEADER: Clean & Centered */
    .main-header {
        text-align: center;
        background: -webkit-linear-gradient(#ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
    }

    /* 4. CHAT BUBBLES: Modern & Floating */
    .stChatMessage {
        padding: 1.2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }

    /* 🤖 AI MESSAGES (LEFT) - Glassy White */
    div[data-testid="stChatMessage"]:nth-of-type(odd) {
        margin-right: auto !important;
        margin-left: 0 !important;
        background-color: rgba(255, 255, 255, 0.9);
        border-left: 5px solid #23a6d5; /* Cyan Accent */
        flex-direction: row !important;
        text-align: left;
    }

    /* 👤 USER MESSAGES (RIGHT) - Glassy Dark Blue */
    div[data-testid="stChatMessage"]:nth-of-type(even) {
        margin-left: auto !important;
        margin-right: 0 !important;
        background-color: rgba(24, 40, 72, 0.9); /* Dark Blue */
        border-right: 5px solid #e73c7e; /* Pink Accent */
        flex-direction: row-reverse !important;
        text-align: right;
        color: white; /* White text for user */
    }

    /* Fix text color inside User bubbles (since background is dark) */
    div[data-testid="stChatMessage"]:nth-of-type(even) p {
        color: white !important;
    }

    /* 5. INPUT BOX: Floating Pill Style */
    .stChatInput input {
        border-radius: 30px !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
        background-color: rgba(255,255,255,0.9) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 6. BUTTON: Gradient Pill */
    div.stButton > button {
        background: linear-gradient(90deg, #23a6d5 0%, #23d5ab 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 1.5rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(35, 213, 171, 0.4);
    }

    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📂 Knowledge Hub</h2>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

    if uploaded_file is not None:
        st.write("")  # Spacer
        if st.button("✨ Ingest & Memorize", type="primary"):
            with st.spinner("🔮 LIRA is learning..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success("✅ Knowledge Acquired!")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"⚠️ Connection failed: {e}")

    st.markdown("---")
    st.caption("🔒 **Secure Environment:** LIRA operates 100% locally. No data leaves this machine.")

# --- MAIN PAGE ---
st.markdown('<h1 class="main-header">✨ LIRA <span style="font-size: 2rem; opacity: 0.7;">| AI Agent</span></h1>',
            unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I am **LIRA**. I'm ready to answer questions about your documents."}
    ]

# Display chat messages
for message in st.session_state.messages:
    # Custom aesthetic avatars
    avatar = "👤" if message["role"] == "user" else "✨"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Get answer
    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🌀 *Thinking...*")

        try:
            payload = {"q": prompt, "top_k": 5}
            response = requests.post(f"{API_URL}/query", data=payload)

            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "No answer found.")

                # Show answer directly (Clean)
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                message_placeholder.error("⚠️ Backend Error")
        except Exception as e:
            message_placeholder.error(f"🔌 Connection Error: {e}")