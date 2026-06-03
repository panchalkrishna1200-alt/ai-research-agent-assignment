# 🤖 AI Research & Recommendation Agent

AI-powered company intelligence report generator — **free, no credit card, cloud deployable**.

## 🚀 Deploy to Streamlit Cloud (Free)

### Step 1 — Get Free Groq API Key
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Click "API Keys" → "Create API Key"
4. Copy the key (starts with `gsk_`)

### Step 2 — Push to GitHub
1. Create a new GitHub repository
2. Upload all files from this folder

### Step 3 — Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub repo
4. Set main file: `app.py`
5. Click Deploy!

### Step 4 — Use the App
1. Open your deployed URL
2. Paste Groq API key in sidebar
3. Enter company name
4. Click Generate Report!

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
ai_research_agent_groq/
├── app.py               ← Main Streamlit UI
├── research.py          ← DuckDuckGo + Wikipedia
├── analyzer.py          ← Groq API integration
├── report_generator.py  ← PDF + Markdown export
├── requirements.txt     ← Dependencies
└── README.md
```

---

## 🛠️ Architecture

```
Company Name Input
      │
      ▼
Research Layer
  ├── DuckDuckGo (4 queries)
  └── Wikipedia summary
      │
      ▼
Groq LLM (5 focused prompts)
  ├── Company Overview
  ├── Key Business Info
  ├── Business Challenges
  ├── AI Opportunities
  └── CEO Pitch
      │
      ▼
Download: PDF / Markdown
```

---

## Free Stack

| Tool | Purpose | Cost |
|------|---------|------|
| Groq API | LLM inference | Free |
| DuckDuckGo | Web search | Free |
| Wikipedia | Company info | Free |
| Streamlit Cloud | Hosting | Free |
| ReportLab | PDF export | Free |
