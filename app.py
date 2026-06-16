"""
app.py  ·  Toyota Pakistan RAG Chatbot
Run with:  streamlit run app.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from pathlib import Path
from rag_engine import build_vector_store, ask

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title  = "Toyota Pakistan Assistant",
    page_icon   = "🚗",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* ── Root palette ── */
:root {
    --toyota-red:    #EB0A1E;
    --toyota-dark:   #1A1A1A;
    --toyota-mid:    #2C2C2C;
    --toyota-silver: #F5F5F5;
    --toyota-muted:  #888888;
    --bubble-user:   #EB0A1E;
    --bubble-bot:    #FFFFFF;
    --accent-line:   rgba(235,10,30,0.15);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #F0F0F0;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--toyota-dark) !important;
    border-right: 1px solid #333;
}
[data-testid="stSidebar"] * { color: #EEEEEE !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
[data-testid="stSidebar"] .stButton button {
    background: var(--toyota-red) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin-top: 4px !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: #c0001a !important;
}

/* ── Top header bar ── */
.toyota-header {
    background: var(--toyota-dark);
    padding: 18px 32px;
    display: flex;
    align-items: center;
    gap: 16px;
    border-bottom: 3px solid var(--toyota-red);
    margin-bottom: 0;
}
.toyota-header .logo-oval {
    background: var(--toyota-red);
    border-radius: 50%;
    width: 44px; height: 44px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.toyota-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.3px;
}
.toyota-header p {
    font-size: 0.78rem;
    color: #AAAAAA;
    margin: 2px 0 0 0;
}

/* ── Chat container ── */
.chat-wrapper {
    max-width: 860px;
    margin: 24px auto 120px auto;
    padding: 0 16px;
}

/* ── Chat bubbles ── */
.msg-row {
    display: flex;
    margin-bottom: 18px;
    align-items: flex-end;
    gap: 10px;
}
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.bot   { flex-direction: row; }

.avatar {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.avatar.user { background: var(--toyota-red); }
.avatar.bot  { background: var(--toyota-dark); border: 2px solid #444; }

.bubble {
    max-width: 76%;
    padding: 14px 18px;
    border-radius: 18px;
    font-size: 0.93rem;
    line-height: 1.65;
}
.bubble.user {
    background: var(--toyota-red);
    color: #FFFFFF;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: #FFFFFF;
    color: var(--toyota-dark);
    border-bottom-left-radius: 4px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 3px solid var(--toyota-red);
}
.bubble.bot ul { padding-left: 18px; margin: 6px 0; }
.bubble.bot li { margin-bottom: 4px; }
.bubble.bot strong { color: var(--toyota-red); }

/* ── Typing indicator ── */
.typing-dots span {
    display: inline-block;
    width: 7px; height: 7px;
    margin: 0 2px;
    background: var(--toyota-red);
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%,60%,100% { transform: translateY(0); }
    30%          { transform: translateY(-8px); }
}

/* ── Input box override ── */
[data-testid="stChatInput"] {
    border-top: 2px solid var(--toyota-red) !important;
    background: #FFFFFF !important;
    padding: 12px 16px !important;
}
[data-testid="stChatInputTextArea"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
}

/* ── Suggested chips ── */
.chip-grid {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin-bottom: 24px;
}
.chip {
    background: #FFFFFF;
    border: 1px solid #DDDDDD;
    border-radius: 20px;
    padding: 7px 14px;
    font-size: 0.82rem;
    color: var(--toyota-dark);
    cursor: pointer;
    transition: all 0.18s;
    font-family: 'Inter', sans-serif;
}
.chip:hover {
    border-color: var(--toyota-red);
    color: var(--toyota-red);
    background: #FFF5F5;
}

/* ── Welcome card ── */
.welcome-card {
    background: linear-gradient(135deg, #1A1A1A 0%, #2C2C2C 100%);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 28px;
    border-left: 4px solid var(--toyota-red);
    color: white;
}
.welcome-card h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    margin: 0 0 8px 0;
    color: #FFFFFF;
}
.welcome-card p { color: #AAAAAA; margin: 0; font-size: 0.9rem; line-height: 1.6; }
.welcome-card .red { color: var(--toyota-red); font-weight: 600; }

/* ── Sidebar model cards ── */
.model-card {
    background: #2C2C2C;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
    border-left: 3px solid var(--toyota-red);
}
.model-card .name { font-weight: 600; font-size: 0.88rem; color: #FFFFFF; }
.model-card .price { font-size: 0.78rem; color: #AAAAAA; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)


# ── Load vector store (cached) ─────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_collection():
    return build_vector_store()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚗 Toyota Pakistan")
    st.markdown("---")

    st.markdown("### 📋 Available Models")
    models = [
        ("Toyota Yaris",               "PKR 4.6M – 5.9M"),
        ("Toyota Corolla Altis",       "PKR 6.3M – 8.0M"),
        ("Corolla Cross Hybrid",       "PKR 10.5M"),
        ("Toyota Fortuner",            "PKR 13.0M – 19.0M"),
        ("Toyota Hilux",               "PKR 7.5M – 17.0M"),
        ("Toyota Hiace",               "PKR 8.3M+"),
    ]
    for name, price in models:
        st.markdown(f"""
        <div class="model-card">
            <div class="name">{name}</div>
            <div class="price">{price}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This AI assistant uses **Retrieval-Augmented Generation (RAG)**
    with **Google Gemini** to answer your Toyota queries
    based on official Pakistan market data.

    **PDC Semester Project**
    """)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#555;'>Powered by Gemini 1.5 Flash · ChromaDB · LangChain</div>",
        unsafe_allow_html=True,
    )


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="toyota-header">
    <div class="logo-oval">🚘</div>
    <div>
        <h1>Toyota Pakistan Assistant</h1>
        <p>Ask me anything about Toyota vehicles — specs, prices, comparisons, maintenance & more</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Load collection with spinner ───────────────────────────────────────────────
with st.spinner("⚙️ Loading Toyota knowledge base …"):
    collection = get_collection()


# ── Chat area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Welcome card (shown only when no messages yet)
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h2>👋 Welcome to ToyotaBot!</h2>
        <p>
            I can help you with <span class="red">prices</span>,
            <span class="red">specifications</span>,
            <span class="red">fuel economy</span>,
            <span class="red">model comparisons</span>,
            <span class="red">maintenance schedules</span>,
            <span class="red">warranty information</span>, and buying advice —
            all tailored for the <span class="red">Pakistan market</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggested questions as clickable chips
    st.markdown("**Try asking:**")
    suggested = [
        "What is the fuel economy of Toyota Corolla?",
        "Difference between Yaris and Corolla Altis?",
        "Which Toyota is best for a family?",
        "Which models have automatic transmission?",
        "What is the Corolla Cross Hybrid price?",
        "Toyota Fortuner maintenance schedule?",
        "Which Toyota gives best fuel efficiency?",
        "What safety features does Yaris have?",
    ]
    cols = st.columns(2)
    for i, q in enumerate(suggested):
        if cols[i % 2].button(q, key=f"chip_{i}"):
            st.session_state.messages.append({"role": "user", "content": q})
            with st.spinner("Thinking …"):
                answer = ask(q, collection)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()


# ── Render chat history ────────────────────────────────────────────────────────
def render_bubble(role: str, content: str):
    if role == "user":
        st.markdown(f"""
        <div class="msg-row user">
            <div class="avatar user">👤</div>
            <div class="bubble user">{content}</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Convert markdown-ish to basic HTML for the bubble
        html_content = content.replace("\n", "<br>")
        st.markdown(f"""
        <div class="msg-row bot">
            <div class="avatar bot">🚗</div>
            <div class="bubble bot">{html_content}</div>
        </div>""", unsafe_allow_html=True)


for msg in st.session_state.messages:
    render_bubble(msg["role"], msg["content"])

st.markdown("</div>", unsafe_allow_html=True)


# ── Chat input ─────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about any Toyota model, price, specs, or comparison …"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_bubble("user", prompt)

    with st.spinner("🔍 Searching knowledge base …"):
        answer = ask(prompt, collection)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    render_bubble("assistant", answer)
    st.rerun()
