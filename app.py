import streamlit as st
import time
from src.agents.agent import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (New Obsidian & Cyber Minimalist Theme) ────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base Reset & App Layout ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #e2e8f0;
}

.stApp {
    background: #090d16;
    background-image:
        radial-gradient(circle at 15% 15%, rgba(6, 182, 212, 0.08), transparent 25%),
        radial-gradient(circle at 85% 85%, rgba(99, 102, 241, 0.08), transparent 25%),
        linear-gradient(180deg, #090d16 0%, #05080f 100%);
}

/* ── Hide Streamlit Elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 3rem 4rem 4rem; max-width: 1300px; }

/* ── Premium Hero Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #06b6d4;
    margin-bottom: 0.8rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4.2rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #06b6d4 0%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 400;
    color: #94a3b8;
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Elegant Thin Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 2.5rem 0;
}

/* ── Unified Layout Containers ── */
.input-card {
    background: rgba(13, 20, 35, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 2.2rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

/* ── Form Controls Customization ── */
.stTextInput > div > div > input {
    background: rgba(5, 8, 15, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #06b6d4 !important;
    box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.15) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #94a3b8 !important;
    margin-bottom: 0.5rem !important;
}

/* ── Dynamic High-Tech Button ── */
.stButton > button {
    background: linear-gradient(135deg, #06b6d4 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(6, 182, 212, 0.15) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 25px rgba(6, 182, 212, 0.3) !important;
    filter: brightness(1.05);
}
.stButton > button:active {
    transform: translateY(1px) !important;
}

/* ── Minimalist Pipeline Step Cards ── */
.step-card {
    background: rgba(13, 20, 35, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    transition: all 0.25s ease;
}
.step-card:hover {
    border-color: rgba(255, 255, 255, 0.08);
    background: rgba(13, 20, 35, 0.5);
}
.step-card.active {
    border-color: rgba(6, 182, 212, 0.3);
    background: rgba(6, 182, 212, 0.03);
}
.step-card.done {
    border-color: rgba(16, 185, 129, 0.2);
    background: rgba(16, 185, 129, 0.02);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: transparent;
}
.step-card.active::before { background: #06b6d4; }
.step-card.done::before   { background: #10b981; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: #64748b;
}
.step-card.active .step-num { color: #06b6d4; }
.step-card.done .step-num { color: #10b981; }

.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    color: #e2e8f0;
}
.step-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.05em;
}
.status-waiting  { color: #475569; }
.status-running  { color: #06b6d4; animation: pulse 2s infinite; }
.status-done     { color: #10b981; }

@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

/* ── Output & Result Panels ── */
.result-panel {
    background: #0d1323;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.8rem 0;
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.result-content {
    font-size: 0.9rem;
    line-height: 1.7;
    color: #cbd5e1;
    white-space: pre-wrap;
}

/* ── Main Reports Structure ── */
.report-panel, .feedback-panel {
    background: rgba(13, 20, 35, 0.5);
    border-radius: 16px;
    padding: 2.5rem;
    margin-top: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
.report-panel { border: 1px solid rgba(6, 182, 212, 0.15); }
.feedback-panel { border: 1px solid rgba(16, 185, 129, 0.15); }

.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    padding-bottom: 0.8rem;
}
.panel-label.orange { color: #06b6d4; border-bottom: 1px solid rgba(6, 182, 212, 0.1); }
.panel-label.green { color: #10b981; border-bottom: 1px solid rgba(16, 185, 129, 0.1); }

/* ── Streamlit Expander Fine-Tuning ── */
details {
    background: rgba(13, 20, 35, 0.25) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.04) !important;
    margin-bottom: 0.8rem;
}
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #94a3b8 !important;
    padding: 0.5rem 1rem !important;
}

/* ── Section Typo ── */
.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: #ffffff;
    margin: 1.5rem 0 1rem;
    letter-spacing: -0.01em;
}

/* ── Elegant Footer ── */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #475569;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }

    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.8rem;color:#64748b;margin-top:0.25rem;font-weight:300;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Researcher<span>Agent</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>

<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:

    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Roadmap for AGI development in next 5 years",
        key="topic_input",
        label_visibility="visible",
    )

    run_btn = st.button(
        "⚡ Run Research Pipeline",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;align-items:center;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#475569;letter-spacing:0.1em;margin-right:0.2rem;">
            SUGGESTIONS //
        </span>
    """, unsafe_allow_html=True)

    examples = [
        "Future of LLM in Tech Industry",
        "All Latest AI Agents in 2026",
        "Roadmap for AGI development in next 5 years",
    ]

    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(255,255,255,0.02);
            border:1px solid rgba(255,255,255,0.05);
            border-radius:6px;
            padding:0.3rem 0.65rem;
            font-size:0.75rem;
            color:#94a3b8;
            font-family:'Plus Jakarta Sans',sans-serif;
            cursor:default;
        ">
            {ex}
        </span>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:

    st.markdown(
        '<div class="section-heading">Pipeline Status</div>',
        unsafe_allow_html=True
    )

    r = st.session_state.results
    done = st.session_state.done

    def s(step):

        if not r:
            return "waiting"

        steps = ["search", "reader", "writer", "critic"]

        if step in r:
            return "done"

        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"

        return "waiting"

    step_card(
        "01",
        "Search Agent",
        s("search"),
        "Gathers recent web information"
    )

    step_card(
        "02",
        "Reader Agent",
        s("reader"),
        "Scrapes & extracts deep content"
    )

    step_card(
        "03",
        "Writer Chain",
        s("writer"),
        "Drafts the full research report"
    )

    step_card(
        "04",
        "Critic Chain",
        s("critic"),
        "Reviews & scores the report"
    )


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍 Search Agent is working…"):

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                ("user",
                 f"Find recent, reliable and detailed information about: {topic_val}")
            ]
        })

        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("📄 Reader Agent is scraping top resources…"):

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })

        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️ Writer is drafting the report…"):

        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })

        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐 Critic is reviewing the report…"):

        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })

        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Generated Outputs</div>',
        unsafe_allow_html=True
    )

    # Raw outputs
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Search Agent Output
                    </div>

                    <div class="result-content">
                        {r["search"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Reader Agent Output
                    </div>

                    <div class="result-content">
                        {r["reader"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    # Final report
    if "writer" in r:

        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">
                📝 Final Research Report
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["writer"])

        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:

        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">
                🧐 Critic Feedback
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["critic"])

        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchAgent // Powered by LangChain multi-agent pipeline // Built with Streamlit
</div>
""", unsafe_allow_html=True)