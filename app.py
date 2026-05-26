# =============================================================================
# DecodeLabs | Batch 2026 | Project 1: Rule-Based AI Chatbot
# Built independently by Egwuatu Chibuike Dominion
# File: app.py — Streamlit Frontend
# =============================================================================

import streamlit as st
import datetime
from chatbot import sanitize_input, get_response, KNOWLEDGE_BASE

st.set_page_config(
    page_title="RuleBot — by Egwuatu Chibuike Dominion",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    /* ── App background ── */
    .stApp {
        background: linear-gradient(135deg, #0d0d1a 0%, #0a1628 50%, #0d0d1a 100%);
        font-family: 'JetBrains Mono', 'Courier New', monospace;
    }
    .block-container {
        max-width: 820px !important;
        padding: 0.8rem 1.5rem 1.5rem 1.5rem !important;
    }

    /* ── HEADER ── */
    .rulebot-header { text-align: center; padding: 0.8rem 0 0.5rem 0; }
    .rulebot-header h1 {
        color: #00e5ff;
        font-size: clamp(1.5rem, 4vw, 2.1rem);
        font-weight: 700; letter-spacing: 3px;
        text-shadow: 0 0 24px rgba(0,229,255,0.45);
        margin: 0;
    }
    .rulebot-header .sub {
        color: #4caf50; font-size: clamp(0.55rem, 1.4vw, 0.7rem);
        letter-spacing: 2.5px; margin: 4px 0 2px 0;
    }
    .rulebot-header .credit {
        color: rgba(0,229,255,0.4);
        font-size: clamp(0.5rem, 1.2vw, 0.6rem);
        letter-spacing: 1px; margin: 0;
    }

    /* ── BADGES ── */
    .status-bar {
        display: flex; justify-content: center;
        gap: 0.5rem; margin: 0.6rem 0 0.9rem; flex-wrap: wrap;
    }
    .status-badge {
        background: rgba(0,229,255,0.07);
        border: 1px solid rgba(0,229,255,0.22);
        border-radius: 20px; padding: 3px 11px;
        font-size: clamp(0.56rem, 1.3vw, 0.66rem);
        color: #00e5ff; letter-spacing: 0.8px; white-space: nowrap;
    }
    .status-badge.green {
        background: rgba(76,175,80,0.07);
        border-color: rgba(76,175,80,0.28); color: #4caf50;
    }

    /* ── STATS BAR — built into main page ── */
    .stats-bar {
        display: flex; gap: 0.6rem; margin-bottom: 0.8rem; flex-wrap: wrap;
    }
    .stat-card {
        flex: 1; min-width: 80px;
        background: rgba(0,180,210,0.07);
        border: 1px solid rgba(0,180,210,0.2);
        border-radius: 8px; padding: 8px 10px;
        text-align: center;
    }
    .stat-card .stat-val {
        color: #00e5ff; font-size: 1.3rem; font-weight: 700;
        display: block; line-height: 1.1;
    }
    .stat-card .stat-lbl {
        color: rgba(180,220,235,0.5);
        font-size: 0.58rem; letter-spacing: 1px;
        display: block; margin-top: 3px;
    }
    .stat-status {
        display: flex; align-items: center; gap: 6px;
        font-size: 0.62rem; margin-top: 4px;
    }

    /* ── CHAT ── */
    .chat-container {
        background: rgba(8,14,28,0.7);
        border: 1px solid rgba(0,229,255,0.13);
        border-radius: 12px; padding: 1rem;
        margin-bottom: 0.8rem;
        height: clamp(300px, 44vh, 420px);
        overflow-y: auto; width: 100%;
    }
    .msg-row {
        display: flex; margin-bottom: 0.75rem;
        align-items: flex-end; gap: 7px;
    }
    .msg-row.user { flex-direction: row-reverse; }
    .avatar {
        width: 28px; height: 28px; border-radius: 50%;
        display: flex; align-items: center;
        justify-content: center; font-size: 12px; flex-shrink: 0;
    }
    .avatar.bot  { background: rgba(0,229,255,0.12); border: 1px solid rgba(0,229,255,0.28); }
    .avatar.user { background: rgba(76,175,80,0.12); border: 1px solid rgba(76,175,80,0.28); }
    .bubble {
        max-width: min(76%, 500px);
        padding: 8px 13px; border-radius: 14px;
        font-size: clamp(0.8rem, 2vw, 0.88rem);
        line-height: 1.6; white-space: pre-wrap; word-break: break-word;
    }
    .bubble.bot {
        background: rgba(0,28,48,0.88);
        border: 1px solid rgba(0,229,255,0.18);
        color: #cfe8f0; border-bottom-left-radius: 4px;
    }
    .bubble.user {
        background: rgba(8,34,18,0.88);
        border: 1px solid rgba(76,175,80,0.22);
        color: #b8dfc0; border-bottom-right-radius: 4px;
    }
    .rule-tag {
        font-size: 0.58rem; color: rgba(0,229,255,0.25);
        margin-top: 2px; padding-left: 35px;
    }
    .rule-tag.user-tag {
        text-align: right; padding-right: 35px;
        padding-left: 0; color: rgba(76,175,80,0.25);
    }
    .timestamp {
        font-size: 0.54rem; color: rgba(255,255,255,0.15);
        text-align: center; margin: 0.3rem 0;
    }

    /* ── INPUT ── */
    .stTextInput > div > div > input {
        background: #0f1b2d !important;
        border: 1.5px solid #253d5a !important;
        border-radius: 8px !important;
        color: #deeef5 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: clamp(0.82rem, 2vw, 0.92rem) !important;
        padding: 0.65rem 1rem !important;
        caret-color: #00e5ff !important;
        width: 100% !important;
    }
    .stTextInput > div > div > input:focus {
        background: #132030 !important;
        border-color: #00b4cc !important;
        box-shadow: 0 0 0 3px rgba(0,180,204,0.1) !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #3d6880 !important; font-style: italic;
        font-size: clamp(0.72rem, 1.8vw, 0.82rem) !important;
    }

    /* ── SEND button ── */
    .stButton > button {
        background: #0b1f35 !important;
        border: 1.5px solid #00b4cc !important;
        color: #00e5ff !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: clamp(0.7rem, 1.6vw, 0.8rem) !important;
        letter-spacing: 1px !important;
        height: 44px !important;
        transition: all 0.18s !important;
        white-space: nowrap !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #102840 !important;
        border-color: #00e5ff !important;
        box-shadow: 0 0 14px rgba(0,229,255,0.25) !important;
    }

    /* ── QUICK COMMANDS grid ── */
    .cmd-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 6px; margin-top: 6px;
    }
    .cmd-pill {
        background: rgba(0,180,210,0.07);
        border: 1px solid rgba(0,180,210,0.22);
        border-radius: 6px; padding: 6px 10px;
        font-size: 0.7rem; color: #7dd3e8;
        cursor: pointer; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
        transition: all 0.15s; font-family: 'JetBrains Mono', monospace;
        text-align: left;
    }
    .cmd-pill:hover {
        background: rgba(0,180,210,0.18);
        border-color: #00e5ff; color: #00e5ff;
    }

    /* ── EXPANDER — for quick commands & knowledge base ── */
    [data-testid="stExpander"] {
        background: rgba(0,180,210,0.04) !important;
        border: 1px solid rgba(0,180,210,0.18) !important;
        border-radius: 10px !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stExpander"] summary {
        color: #00c8e0 !important;
        font-size: 0.74rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        padding: 10px 14px !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: #00e5ff !important;
        background: rgba(0,200,224,0.06) !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] details[open] summary {
        border-bottom: 1px solid rgba(0,180,210,0.15) !important;
        border-radius: 10px 10px 0 0 !important;
    }

    /* ── MOBILE ── */
    @media (max-width: 640px) {
        .block-container { padding: 0.5rem 0.7rem 1rem !important; }
        .chat-container { height: 52vh !important; padding: 0.7rem !important; }
        .bubble { max-width: 90% !important; font-size: 0.82rem !important; }
        .stats-bar { gap: 0.4rem !important; }
        .stat-card .stat-val { font-size: 1.1rem !important; }
        .cmd-grid { grid-template-columns: repeat(2, 1fr) !important; }
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.14); border-radius: 4px; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

if "messages" not in st.session_state:
    st.session_state.messages       = []
    st.session_state.session_active = True
    st.session_state.message_count  = 0
    st.session_state.matched_rules  = 0
    st.session_state.fallback_count = 0
    st.session_state.session_start  = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "bot",
        "content": "Hello! I'm RuleBot 🤖\nBuilt independently by Egwuatu Chibuike Dominion.\nType 'help' to see what I can do, or just say hello!",
        "rule": "welcome rule",
        "time": datetime.datetime.now().strftime("%H:%M")
    })

if "input_key" not in st.session_state:
    st.session_state.input_key = 0


# =============================================================================
# HELPER — process a message (reused for quick cmds and typed input)
# =============================================================================

def process_message(raw: str):
    st.session_state.messages.append({
        "role": "user", "content": raw,
        "rule": "user input",
        "time": datetime.datetime.now().strftime("%H:%M")
    })
    st.session_state.message_count += 1
    clean = sanitize_input(raw)
    response, is_exit = get_response(clean)
    matched_rule = None
    for keyword in KNOWLEDGE_BASE:
        if keyword in clean:
            matched_rule = f"{keyword} rule"
            st.session_state.matched_rules += 1
            break
    if matched_rule is None:
        matched_rule = "fallback rule"
        st.session_state.fallback_count += 1
    st.session_state.messages.append({
        "role": "bot", "content": response,
        "rule": matched_rule,
        "time": datetime.datetime.now().strftime("%H:%M")
    })
    if is_exit:
        st.session_state.session_active = False
    st.session_state.input_key += 1
    st.rerun()


# =============================================================================
# HEADER
# =============================================================================

st.markdown("""
<div class="rulebot-header">
    <h1>⚡ RULEBOT</h1>
    <p class="sub">RULE-BASED AI CHATBOT &nbsp;|&nbsp; PROJECT 1 &nbsp;|&nbsp; DECODELABS BATCH 2026</p>
    <p class="credit">Built independently by Egwuatu Chibuike Dominion &nbsp;·&nbsp; Coding from the roadmap up</p>
</div>
<div class="status-bar">
    <span class="status-badge green">● ONLINE</span>
    <span class="status-badge">DICTIONARY O(1)</span>
    <span class="status-badge">IPO MODEL</span>
    <span class="status-badge">ZERO HALLUCINATIONS</span>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# STATS BAR — always visible, no sidebar needed
# =============================================================================

sc    = "#4caf50" if st.session_state.session_active else "#ff6b6b"
stxt  = "● ACTIVE"   if st.session_state.session_active else "● ENDED"
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-card">
        <span class="stat-val">{st.session_state.message_count}</span>
        <span class="stat-lbl">MESSAGES</span>
    </div>
    <div class="stat-card">
        <span class="stat-val">{st.session_state.matched_rules}</span>
        <span class="stat-lbl">RULES HIT</span>
    </div>
    <div class="stat-card">
        <span class="stat-val">{st.session_state.fallback_count}</span>
        <span class="stat-lbl">FALLBACKS</span>
    </div>
    <div class="stat-card" style="flex:2; text-align:left; padding:8px 14px">
        <span class="stat-lbl">SESSION STARTED</span>
        <span class="stat-val" style="font-size:0.85rem; margin-top:3px">
            {st.session_state.session_start}
        </span>
        <span style="color:{sc}; font-size:0.65rem; font-weight:700; display:block; margin-top:4px">
            {stxt}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# CHAT MESSAGES
# =============================================================================

chat_html = '<div class="chat-container">'
for i, msg in enumerate(st.session_state.messages):
    role    = msg["role"]
    content = msg["content"]
    rule    = msg.get("rule", "")
    time    = msg.get("time", "")
    icon    = "🤖" if role == "bot" else "👤"
    bc      = "bot" if role == "bot" else "user"
    tc      = "rule-tag" if role == "bot" else "rule-tag user-tag"
    if i == 0 or i % 6 == 0:
        chat_html += f'<div class="timestamp">── {time} ──</div>'
    chat_html += f"""
    <div class="msg-row {role}">
        <div class="avatar {bc}">{icon}</div>
        <div class="bubble {bc}">{content}</div>
    </div>"""
    if rule:
        chat_html += f'<div class="{tc}">⚙ {rule}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

if not st.session_state.session_active:
    st.markdown("""
    <div style='text-align:center; padding:0.7rem;
    background:rgba(76,175,80,0.07); border:1px solid rgba(76,175,80,0.2);
    border-radius:8px; margin:0.4rem 0'>
        <p style='color:#4caf50; font-size:0.76rem; margin:0'>
        ✅ SESSION ENDED — Click "🔄 New Session" below to restart
        </p>
    </div>""", unsafe_allow_html=True)


# =============================================================================
# INPUT AREA
# =============================================================================

if st.session_state.session_active:
    ci, cb = st.columns([5, 1])
    with ci:
        user_input = st.text_input(
            label="input",
            placeholder="Type your message...  (e.g. hello · tell me a joke · bye)",
            label_visibility="collapsed",
            key=f"chat_input_{st.session_state.input_key}",
        )
    with cb:
        send = st.button("SEND →", use_container_width=True, key="send_btn")

    if send and user_input.strip():
        process_message(user_input.strip())


# =============================================================================
# QUICK COMMANDS — expandable section on main page
# =============================================================================

with st.expander("⚡  QUICK COMMANDS — click any to send instantly", expanded=False):
    quick_cmds = [
        ("👋", "hello"),
        ("😄", "tell me a joke"),
        ("🤔", "what can you do"),
        ("💪", "motivate me"),
        ("🧠", "what is ai"),
        ("🕐", "what time is it"),
        ("📅", "what is today"),
        ("📐", "what is ipo model"),
        ("⚡", "what is o1"),
        ("🤖", "who are you"),
        ("❓", "help"),
        ("🚪", "bye"),
    ]
    cols = st.columns(3)
    for idx, (icon, cmd) in enumerate(quick_cmds):
        with cols[idx % 3]:
            if st.button(f"{icon}  {cmd}", key=f"qcmd_{cmd}", use_container_width=True):
                if st.session_state.session_active:
                    process_message(cmd)


# =============================================================================
# ARCHITECTURE & KNOWLEDGE BASE — expandable sections
# =============================================================================

with st.expander("⚙️  ARCHITECTURE & HOW IT WORKS", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<p style='color:#00c8e0; font-size:0.72rem; font-weight:700; margin:0 0 8px 0'>IPO PIPELINE</p>", unsafe_allow_html=True)
        for step, desc in [
            ("1. INPUT",    "Raw user message"),
            ("2. SANITIZE", "lower() + strip()"),
            ("3. MATCH",    "Dictionary O(1)"),
            ("4. RESPOND",  "Return matched reply"),
            ("5. FALLBACK", ".get() default"),
            ("6. LOOP",     "while True + break"),
        ]:
            st.markdown(
                f"<p style='color:rgba(180,215,228,0.58); font-size:0.69rem; margin:3px 0'>"
                f"<span style='color:#00e5ff'>{step}</span> — {desc}</p>",
                unsafe_allow_html=True
            )
    with c2:
        st.markdown("<p style='color:#00c8e0; font-size:0.72rem; font-weight:700; margin:0 0 8px 0'>KEY PATTERNS</p>", unsafe_allow_html=True)
        for label, val in [
            ("Approach",   "Dictionary, not if-elif"),
            ("Complexity", "O(1) vs O(n)"),
            ("Safety",     "Zero hallucinations"),
            ("Type",       "White Box AI"),
            ("Loop",       "while True + break"),
            ("Exit",       "bye / quit / goodbye"),
        ]:
            st.markdown(
                f"<p style='color:rgba(180,215,228,0.58); font-size:0.69rem; margin:3px 0'>"
                f"<span style='color:#00c8e0'>{label}:</span> {val}</p>",
                unsafe_allow_html=True
            )

with st.expander("📚  KNOWLEDGE BASE", expanded=False):
    categories = {
        "Greetings":   ["hello","hi","hey","good morning","good afternoon"],
        "Identity":    ["what is your name","who are you","who made you"],
        "Status":      ["how are you","are you ok"],
        "Help":        ["what can you do","help"],
        "Jokes":       ["tell me a joke","joke"],
        "Motivation":  ["motivate me","inspire me","i feel sad"],
        "AI Concepts": ["what is ai","what is ipo model","what is o1"],
        "Time/Date":   ["what time is it","what is today"],
        "Gratitude":   ["thank you","thanks"],
        "Exit":        ["bye","goodbye","exit","quit"],
    }
    total = sum(len(v) for v in categories.values())
    st.markdown(f"<p style='color:#4caf50; font-size:0.66rem; margin:0 0 8px 0'>Total intents: {total}</p>", unsafe_allow_html=True)
    cols = st.columns(2)
    items = list(categories.items())
    for idx, (cat, keys) in enumerate(items):
        with cols[idx % 2]:
            st.markdown(f"<p style='color:#00c8e0; font-size:0.67rem; margin:6px 0 2px 0'>▸ {cat}</p>", unsafe_allow_html=True)
            for k in keys:
                st.markdown(f"<p style='color:rgba(145,192,210,0.42); font-size:0.62rem; margin:0 0 0 8px'>→ {k}</p>", unsafe_allow_html=True)


# =============================================================================
# NEW SESSION + FOOTER
# =============================================================================

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

if st.button("🔄  New Session", use_container_width=True, key="new_session"):
    st.session_state.messages       = []
    st.session_state.session_active = True
    st.session_state.message_count  = 0
    st.session_state.matched_rules  = 0
    st.session_state.fallback_count = 0
    st.session_state.input_key     += 1
    st.session_state.session_start  = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "bot",
        "content": "Hello! I'm RuleBot 🤖\nNew session started. How can I help you?\nType 'help' to see all my capabilities!",
        "rule": "welcome rule",
        "time": datetime.datetime.now().strftime("%H:%M")
    })
    st.rerun()

st.markdown("""
<div style='text-align:center; margin-top:0.8rem; padding:0.6rem;
border-top:1px solid rgba(0,229,255,0.07)'>
    <p style='color:rgba(255,255,255,0.12); font-size:0.58rem; letter-spacing:1.5px; margin:0'>
    BUILT BY EGWUATU CHIBUIKE DOMINION &nbsp;·&nbsp; DECODELABS BATCH 2026 &nbsp;·&nbsp; PROJECT 1
    </p>
    <p style='color:rgba(0,200,224,0.2); font-size:0.55rem; margin:3px 0 0 0'>
    IPO Model &nbsp;|&nbsp; Dictionary O(1) &nbsp;|&nbsp; Zero Hallucinations &nbsp;|&nbsp; White Box AI
    </p>
</div>
""", unsafe_allow_html=True)