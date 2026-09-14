import textwrap
from datetime import datetime

import streamlit as st

from pipeline import run_research_pipeline


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResearchOS",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    textwrap.dedent(
        """
        <style>

        .stApp {
            background: #0b0d12;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        section[data-testid="stSidebar"] {
            background: #10131a;
            border-right: 1px solid #222631;
        }

        .hero {
            padding: 1.5rem 0 1rem 0;
        }

        .hero-title {
            font-size: 3rem;
            font-weight: 750;
            letter-spacing: -1.5px;
            margin-bottom: 0.4rem;
        }

        .hero-subtitle {
            color: #8b93a7;
            font-size: 1.05rem;
        }

        .pipeline {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 1.5rem 0 2rem 0;
            padding: 1rem;
            background: #11151d;
            border: 1px solid #242936;
            border-radius: 14px;
        }

        .agent {
            flex: 1;
            text-align: center;
            padding: 0.8rem;
            background: #171b24;
            border-radius: 10px;
            border: 1px solid #292f3d;
        }

        .agent-icon {
            font-size: 1.5rem;
        }

        .agent-name {
            font-weight: 650;
            margin-top: 0.3rem;
        }

        .agent-desc {
            color: #7f8798;
            font-size: 0.78rem;
        }

        .arrow {
            color: #596173;
            font-size: 1.3rem;
        }

        .input-label {
            color: #aeb6c7;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }

        .report-header {
            background: linear-gradient(
                135deg,
                #151a25,
                #11151d
            );
            border: 1px solid #292f3c;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }

        .status {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 20px;
            background: #17241e;
            color: #78d6a0;
            font-size: 0.8rem;
            font-weight: 600;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        </style>
        """
    ),
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "topic" not in st.session_state:
    st.session_state.topic = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🔬 ResearchOS")

    st.caption("Multi-Agent Research Workspace")

    st.divider()

    st.markdown("### Pipeline")

    st.markdown(
        """
        **🔎 Search Agent**

        Finds recent information using Tavily.

        **📖 Reader Agent**

        Scrapes and analyzes useful sources.

        **✍️ Writer Chain**

        Converts research into a structured report.

        **🧐 Critic Chain**

        Reviews the report and provides feedback.
        """
    )

    st.divider()

    st.markdown("### Recent Research")

    if st.session_state.history:

        for i, item in enumerate(
            reversed(st.session_state.history)
        ):

            if st.button(
                item["topic"],
                key=f"history_{i}",
                use_container_width=True,
            ):
                st.session_state.result = item["result"]
                st.session_state.topic = item["topic"]
                st.rerun()

    else:

        st.caption("No research runs yet.")


# =========================================================
# HERO
# =========================================================

st.markdown(
    textwrap.dedent(
        """
        <div class="hero">

            <div class="hero-title">
                Research anything. Get a report.
            </div>

            <div class="hero-subtitle">
                A multi-agent AI system that searches, reads,
                writes, and critiques research automatically.
            </div>

        </div>
        """
    ),
    unsafe_allow_html=True,
)


# =========================================================
# PIPELINE VISUAL
# =========================================================

st.markdown(
    textwrap.dedent(
        """
        <div class="pipeline">

            <div class="agent">
                <div class="agent-icon">🔎</div>
                <div class="agent-name">Search</div>
                <div class="agent-desc">Find sources</div>
            </div>

            <div class="arrow">→</div>

            <div class="agent">
                <div class="agent-icon">📖</div>
                <div class="agent-name">Reader</div>
                <div class="agent-desc">Analyze sources</div>
            </div>

            <div class="arrow">→</div>

            <div class="agent">
                <div class="agent-icon">✍️</div>
                <div class="agent-name">Writer</div>
                <div class="agent-desc">Write report</div>
            </div>

            <div class="arrow">→</div>

            <div class="agent">
                <div class="agent-icon">🧐</div>
                <div class="agent-name">Critic</div>
                <div class="agent-desc">Review quality</div>
            </div>

        </div>
        """
    ),
    unsafe_allow_html=True,
)


# =========================================================
# RESEARCH INPUT
# =========================================================

st.markdown(
    '<div class="input-label">What do you want to research?</div>',
    unsafe_allow_html=True,
)

topic = st.text_input(
    "Research topic",
    value=st.session_state.topic,
    placeholder="e.g. Latest developments in AI agents",
    label_visibility="collapsed",
)


run = st.button(
    "🚀 Start Research",
    type="primary",
)


# =========================================================
# RUN PIPELINE
# =========================================================

if run:

    if not topic.strip():

        st.warning("Please enter a research topic first.")

    else:

        st.session_state.topic = topic.strip()

        st.markdown("### Research in progress")

        progress = st.progress(0)

        status = st.empty()

        try:

            status.markdown(
                '<span class="status">🔎 Search Agent working...</span>',
                unsafe_allow_html=True,
            )

            progress.progress(10)

            result = run_research_pipeline(
                topic.strip()
            )

            progress.progress(100)

            status.markdown(
                '<span class="status">✓ Research completed</span>',
                unsafe_allow_html=True,
            )

            st.session_state.result = result

            st.session_state.history.append(
                {
                    "topic": topic.strip(),
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "result": result,
                }
            )

            st.success("Research completed successfully.")

        except Exception as e:

            st.error(
                f"Something went wrong while running the pipeline:\n\n{e}"
            )


# =========================================================
# RESULTS
# =========================================================

result = st.session_state.result


if result:

    st.divider()

    st.markdown(
        textwrap.dedent(
            f"""
            <div class="report-header">

                <div style="color:#7f8798;font-size:0.8rem;">
                    RESEARCH REPORT
                </div>

                <div style="
                    font-size:1.8rem;
                    font-weight:700;
                    margin-top:0.3rem;
                ">
                    {st.session_state.topic}
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


    # =====================================================
    # STATUS METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🔎 Search", "Completed")

    with col2:
        st.metric("📖 Reader", "Completed")

    with col3:
        st.metric("✍️ Writer", "Completed")

    with col4:
        st.metric("🧐 Critic", "Completed")


    st.write("")


    # =====================================================
    # RESULT TABS
    # =====================================================

    report_tab, sources_tab, reader_tab, critic_tab = st.tabs(
        [
            "📝 Report",
            "🔎 Sources",
            "📖 Research Analysis",
            "🧐 Critic",
        ]
    )


    # =====================================================
    # REPORT
    # =====================================================

    with report_tab:

        report = result.get("report", "")

        if report:

            st.markdown(report)

            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name=(
                    st.session_state.topic
                    .replace(" ", "_")
                    .lower()
                    + ".md"
                ),
                mime="text/markdown",
            )

        else:

            st.info("No report was generated.")


    # =====================================================
    # SOURCES
    # =====================================================

    with sources_tab:

        st.markdown("### 🔎 Search Results")

        search_results = result.get(
            "search_results",
            "",
        )

        if search_results:

            st.markdown(search_results)

        else:

            st.info("No search results available.")


    # =====================================================
    # READER
    # =====================================================

    with reader_tab:

        st.markdown("### 📖 Reader Agent Analysis")

        reader_results = result.get(
            "reader_results",
            "",
        )

        if reader_results:

            st.markdown(reader_results)

        else:

            st.info("No reader analysis available.")


    # =====================================================
    # CRITIC
    # =====================================================

    with critic_tab:

        st.markdown("### 🧐 Critic Review")

        critique = result.get(
            "critique",
            "",
        )

        if critique:

            st.markdown(critique)

        else:

            st.info("No critic feedback available.")