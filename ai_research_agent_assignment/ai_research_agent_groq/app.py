import streamlit as st
import time
from research import search_company, get_wikipedia_summary
from analyzer import analyze_with_groq
from report_generator import generate_markdown_report, generate_pdf_report

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f, #0d6efd);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 { color: white !important; margin: 0; }
    .main-header p  { color: rgba(255,255,255,0.9) !important; margin: 0.5rem 0 0; }

    .report-section {
        background: white;
        border: 1px solid #e0e0e0;
        border-left: 5px solid #0d6efd;
        border-radius: 0 10px 10px 0;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        color: #1a1a1a !important;
        font-size: 15px;
        line-height: 1.8;
    }
    .report-section.biz        { border-left-color: #0dcaf0; }
    .report-section.challenges { border-left-color: #fd7e14; }
    .report-section.ai-opps    { border-left-color: #6f42c1; }
    .report-section.pitch      { border-left-color: #198754; }

    .report-section p,
    .report-section li,
    .report-section ul,
    .report-section ol,
    .report-section h1,
    .report-section h2,
    .report-section h3,
    .report-section strong,
    .report-section span {
        color: #1a1a1a !important;
    }

    .status-box {
        background: #e8f4fd;
        border: 1px solid #bee5fb;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #0c4a6e;
    }
    .api-box {
        background: #f0fff4;
        border: 1px solid #a3e4b7;
        border-radius: 10px;
        padding: 1rem 1.4rem;
        margin-bottom: 1rem;
    }
    .stExpander { border: 1px solid #e0e0e0 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Research & Recommendation Agent</h1>
    <p>Generate structured intelligence reports for any company — powered by Groq AI + DuckDuckGo</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 Groq API Key")
    st.markdown('<div class="api-box">Get your <b>free</b> key at<br><a href="https://console.groq.com" target="_blank">console.groq.com</a></div>', unsafe_allow_html=True)

    api_key = st.text_input(
        "Enter Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Free at console.groq.com — no credit card needed"
    )

    st.markdown("---")
    model_choice = st.selectbox(
        "🧠 Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
        help="All free on Groq"
    )

    st.markdown("---")
    st.markdown("### 📋 How to use")
    st.markdown("""
1. Get free key at [console.groq.com](https://console.groq.com)
2. Paste key above
3. Enter company name
4. Click **Generate Report**
5. Download PDF or Markdown
    """)

    st.markdown("---")
    st.markdown("### 🔗 Stack")
    st.markdown("""
- ⚡ **Groq** — ultra-fast free LLM
- 🔍 **DuckDuckGo** — web search
- 📖 **Wikipedia** — company info
- 📄 **ReportLab** — PDF export
- 🌐 **Streamlit** — UI
    """)
    st.caption("Free · No credit card · Cloud deployable")

# ── Main Input ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    company_name = st.text_input(
        "🏢 Company Name",
        placeholder="e.g. Adani Realty, Prestige Group, Sobha, Brigade Group...",
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate Report", type="primary", use_container_width=True)

# ── Validation ────────────────────────────────────────────────────────────────
if generate_btn:
    if not api_key.strip():
        st.error("❌ Please enter your Groq API key in the sidebar. Get it free at https://console.groq.com")
        st.stop()
    if not company_name.strip():
        st.warning("⚠️ Please enter a company name.")
        st.stop()

# ── Generate Report ───────────────────────────────────────────────────────────
if generate_btn and api_key.strip() and company_name.strip():
    st.markdown("---")
    progress_bar = st.progress(0)
    status_placeholder = st.empty()

    def update_status(msg, pct):
        status_placeholder.markdown(f'<div class="status-box">⏳ {msg}</div>', unsafe_allow_html=True)
        progress_bar.progress(pct)

    report_data = {}

    try:
        # Step 1 – Research
        update_status(f"Searching the web for '{company_name}'...", 10)
        search_results = search_company(company_name)

        update_status(f"Fetching Wikipedia data...", 20)
        wiki_summary = get_wikipedia_summary(company_name)

        combined_research = f"""
COMPANY: {company_name}

WIKIPEDIA SUMMARY:
{wiki_summary}

WEB SEARCH RESULTS:
{search_results}
        """.strip()

        # Step 2 – Overview
        update_status("Generating company overview...", 35)
        overview = analyze_with_groq(
            api_key, model_choice,
            f"""You are a senior business analyst. Based on the research below, write a detailed Company Overview for {company_name}.

Cover:
- What the company does (core business)
- Industry & sector
- Scale (revenue, employees, number of projects if available)
- Geographic presence and key markets

Research:
{combined_research}

Write in clear professional paragraphs. Be specific and factual. 3-4 paragraphs."""
        )
        report_data["overview"] = overview

        # Step 3 – Key Business Info
        update_status("Extracting key business information...", 50)
        biz_info = analyze_with_groq(
            api_key, model_choice,
            f"""You are a business analyst. Based on the research below, identify key business information for {company_name}.

Include:
- Major products / services / offerings
- Recent developments or news (last 1-2 years)
- Expansion plans or upcoming projects
- Important partnerships, awards, or milestones

Research:
{combined_research}

Use bullet points. Be specific to this company only."""
        )
        report_data["biz_info"] = biz_info

        # Step 4 – Challenges
        update_status("Identifying business challenges...", 63)
        challenges = analyze_with_groq(
            api_key, model_choice,
            f"""You are a strategic business consultant. Based on the research below about {company_name}, identify specific potential business challenges.

For each challenge:
1. Name the challenge clearly
2. Explain WHY it is a challenge for THIS specific company
3. State the business impact

Cover:
- Operational bottlenecks
- Sales & lead generation challenges
- Customer experience challenges
- Market or competitive challenges

Research:
{combined_research}

Be highly specific to {company_name}. Connect each challenge to evidence from the research."""
        )
        report_data["challenges"] = challenges

        # Step 5 – AI Opportunities
        update_status("Identifying AI opportunities...", 76)
        ai_opps = analyze_with_groq(
            api_key, model_choice,
            f"""You are an AI solutions architect. Based on the research and challenges of {company_name}, suggest specific AI-powered solutions.

For each opportunity:
1. Name the AI solution
2. Which specific business problem it solves (from the challenges above)
3. Expected business impact (quantify where possible)
4. Implementation complexity: Low / Medium / High

Cover areas like:
- Sales automation & AI lead scoring
- Customer engagement & AI chatbots
- Document processing & OCR automation
- Predictive analytics & demand forecasting
- Operations & workflow optimization

Research:
{combined_research}

Every suggestion must be specific to {company_name}. No generic answers."""
        )
        report_data["ai_opps"] = ai_opps

        # Step 6 – CEO Pitch
        update_status("Writing personalized CEO pitch...", 88)
        pitch = analyze_with_groq(
            api_key, model_choice,
            f"""Write a personalized one-page pitch letter to the CEO of {company_name}.

Structure:
1. Opening — Why you specifically reached out to {company_name} (reference their business)
2. Opportunities Identified — 2-3 specific business opportunities you found
3. Recommended AI Solutions — What you would implement and the expected ROI
4. Call to Action — A clear next step

Research about the company:
{combined_research}

Tone: Professional, confident, personalized. Address as "Dear CEO" or use their role.
Length: 400-500 words. Make it feel like a real business pitch, not a template."""
        )
        report_data["pitch"] = pitch

        # Done
        progress_bar.progress(100)
        status_placeholder.markdown(
            '<div class="status-box" style="background:#d4edda;border-color:#a3e4b7;color:#155724;">✅ Report generated successfully!</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.8)
        status_placeholder.empty()
        progress_bar.empty()

        # ── Display Report ────────────────────────────────────────────────────
        st.markdown(f"## 📊 Intelligence Report: {company_name}")
        st.caption(f"Generated on {time.strftime('%B %d, %Y at %H:%M')} · Model: {model_choice}")
        st.markdown("---")

        with st.expander("🏢 1. Company Overview", expanded=True):
            st.markdown(f'<div class="report-section">{overview}</div>', unsafe_allow_html=True)

        with st.expander("📋 2. Key Business Information", expanded=True):
            st.markdown(f'<div class="report-section biz">{biz_info}</div>', unsafe_allow_html=True)

        with st.expander("⚠️ 3. Potential Business Challenges", expanded=True):
            st.markdown(f'<div class="report-section challenges">{challenges}</div>', unsafe_allow_html=True)

        with st.expander("🤖 4. AI Opportunities", expanded=True):
            st.markdown(f'<div class="report-section ai-opps">{ai_opps}</div>', unsafe_allow_html=True)

        with st.expander("🎯 5. Personalized CEO Pitch", expanded=True):
            st.markdown(f'<div class="report-section pitch">{pitch}</div>', unsafe_allow_html=True)

        # ── Downloads ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📥 Download Report")
        dl1, dl2 = st.columns(2)

        md_content = generate_markdown_report(company_name, report_data)
        with dl1:
            st.download_button(
                "📄 Download Markdown",
                data=md_content,
                file_name=f"{company_name.replace(' ', '_')}_report.md",
                mime="text/markdown",
                use_container_width=True
            )
        try:
            pdf_bytes = generate_pdf_report(company_name, report_data)
            with dl2:
                st.download_button(
                    "📑 Download PDF",
                    data=pdf_bytes,
                    file_name=f"{company_name.replace(' ', '_')}_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception:
            with dl2:
                st.info("PDF: run `pip install reportlab`")

    except Exception as e:
        progress_bar.empty()
        status_placeholder.empty()
        err = str(e)
        if "401" in err or "invalid_api_key" in err.lower():
            st.error("❌ Invalid Groq API key. Please check and re-enter.")
        elif "rate_limit" in err.lower():
            st.warning("⚠️ Rate limit hit. Wait 30 seconds and try again.")
        else:
            st.error(f"❌ Error: {err}")
