# 🚨 Disaster Response AI Agent

> **An AI-powered disaster monitoring and emergency response coordination system — combining Claude AI, real-time web search, conversation memory, and interactive mapping into a life-safety platform.**

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=flat-square&logo=streamlit)
![Claude AI](https://img.shields.io/badge/Claude-Sonnet%204-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=flat-square)

---

## 📌 Problem Statement

During natural disasters — earthquakes, wildfires, floods, hurricanes — people need fast, reliable, actionable information. But in a crisis:

- Emergency hotlines are overwhelmed and unavailable
- Information is scattered across news sites, government portals, and social media
- People don't know the correct step-by-step safety protocol for their specific situation
- Responders have no unified system to track multiple simultaneous disasters with severity prioritization
- There is no intelligent system that combines real-time information search with personalized emergency guidance in one place

The result: delayed decisions, panic, and preventable harm.

---

## 💡 My Solution

The **Disaster Response AI Agent** is a full-stack AI application that combines:

- **Claude AI (claude-sonnet-4)** — for intelligent, context-aware disaster guidance via natural language
- **Real-time web search** — automatically searches for current disaster information using the `web_search` tool
- **Conversation memory** — maintains full session history for multi-turn emergency consultations
- **Data deduplication** — prevents duplicate disaster entries via a dedicated deduplication engine
- **Severity classification** — scores disasters as Critical / High / Medium / Low with automated recommendations
- **Interactive map view** — geographic visualization of active disasters with coordinate tracking
- **Intelligent fallback system** — 7 disaster-specific response protocols that work even without API access

---

## 📊 Metrics & Capabilities

| Feature | Details |
|---|---|
| **Disaster Types Supported** | Earthquake, Wildfire, Flood, Hurricane, Tornado, Tsunami, and more |
| **Severity Levels** | Critical (4) / High (3) / Medium (2) / Low (1) — auto-scored |
| **Fallback Protocols** | 7 built-in keyword-triggered emergency response templates |
| **Emergency Contacts** | 6 countries pre-loaded (USA, Europe, UK, Australia, India, Canada) |
| **Context Memory** | Up to 100 messages retained per session |
| **Response Timeout** | 30 seconds with graceful fallback |
| **API Model** | claude-sonnet-4-20250514 with web_search_20250305 tool |

---

## 🛠️ Skills & Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.8+ |
| Web UI | Streamlit (responsive, light theme, 3D effects, animations) |
| AI Model | Claude Sonnet 4 (Anthropic API) |
| Web Search | Anthropic `web_search_20250305` tool |
| API Layer | Python `requests` (direct Anthropic API calls) |
| Memory | Custom conversation history manager (`memory.py`) |
| Deduplication | Custom disaster deduplication engine (`depuce.py`) |
| Utilities | Custom severity analyzer, emergency contact system (`utils.py`) |
| Environment | `.env` + `python-dotenv` for secure API key management |
| Dev Environment | VS Code Dev Containers (`.devcontainer`) |
| Setup | `setup.sh` for one-command environment setup |

---

## 📂 Dataset Details

This project uses **live, real-time data** — not a static dataset:

| Source | Type | Details |
|---|---|---|
| **Anthropic web search** | Live web results | Current disaster news, USGS earthquake feeds, weather alerts |
| **Built-in fallback data** | Static templates | 7 disaster-specific safety protocols (earthquake, wildfire, flood, etc.) |
| **Mock disaster tracker** | In-memory | Simulated active disaster tracking (Earthquake CA, Wildfire NSW) with lat/lng |
| **Emergency contacts** | Static | 6-country emergency number database |

---

## 🗂️ Folder Structure

```
Disaster-Management-System/
├── main.py              # Streamlit UI — chat interface, map view, analytics dashboard
├── tools.py             # Claude API integration + web search + fallback responses (360 lines)
├── memory.py            # Conversation history management (session state)
├── utils.py             # Utility functions — input validation, formatting
├── depuce.py            # Disaster data deduplication engine
├── requirements.txt     # Python dependencies
├── setup.sh             # One-command environment setup script
├── .env.example         # API key template (never commit actual keys)
├── .gitignore           # Excludes .env and sensitive files
├── .devcontainer/       # VS Code Dev Container configuration
└── README.md
```

---

## ⚙️ System Architecture

```
Step 1  → User opens Streamlit app → selects Chat / Map / Analytics tab
Step 2  → User types natural language query ("What should I do during a flood?")
Step 3  → tools.py sends message + conversation history to Claude Sonnet 4 API
Step 4  → Claude decides: answer directly OR invoke web_search_20250305 tool
Step 5  → If web search: Claude fetches live disaster news/updates from the web
Step 6  → Claude generates structured, safety-focused response
Step 7  → memory.py appends exchange to session history (up to 100 messages)
Step 8  → If API fails: generate_fallback_response() matches keywords → returns protocol
Step 9  → depuce.py checks incoming disaster data for duplicates before adding to tracker
Step 10 → analyze_disaster_severity() scores event → Critical/High/Medium/Low + recommendation
Step 11 → Map view renders active disasters with coordinates and severity badges
Step 12 → Analytics dashboard shows active count, response metrics, export report button
```

---

## 🔍 Why This Tech Stack?

| Choice | Reason |
|---|---|
| **Claude Sonnet 4** | Best-in-class reasoning for structured, safety-critical responses; supports tool use natively |
| **web_search tool** | Real-time disaster information without managing external APIs separately |
| **Streamlit** | Fastest path to a production-looking UI; no frontend code required |
| **Custom memory.py** | Claude has no built-in session memory — manual history management is required for multi-turn conversations |
| **Fallback system** | Life-safety apps cannot rely solely on API availability — offline protocols are essential |
| **python-dotenv** | Industry best practice for API key management — never hardcode secrets |
| **Dev Containers** | Reproducible development environment — any contributor gets identical setup in one command |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Anthropic API key ([get one here](https://console.anthropic.com))

### Quick Setup
```bash
git clone https://github.com/Mokshitsharma/Disaster-Management-System.git
cd Disaster-Management-System
bash setup.sh
```

### Manual Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Run
```bash
streamlit run main.py
```
Open browser at **http://localhost:8501**

### Example Queries
```
"What disasters are currently active worldwide?"
"What should I do during an earthquake?"
"Help me create an evacuation plan for my family"
"What should be in my emergency kit?"
"Search for recent wildfire news in California"
```

---

## 🔐 Security Notes

> ⚠️ **Important:** The repo contains a `.env.example` file — **never commit your actual API key**. The `.gitignore` excludes `.env` automatically.

1. Always use environment variables — never hardcode API keys in source files
2. Add `.env` to `.gitignore` before your first commit
3. For cloud deployment, use Streamlit Secrets or environment variables in your hosting platform

---

## 🔮 Future Improvements

1. **Real disaster API integration** — connect to USGS Earthquake API, FIRMS (NASA wildfire), GDACS for live global disaster feeds
2. **SMS/Email alert system** — push notifications via Twilio when disasters are detected near user's location
3. **Predictive risk modeling** — ML model to predict disaster severity escalation based on historical patterns
4. **Multi-language support** — translate emergency guidance into Hindi, Spanish, French for broader reach
5. **Mobile app** — React Native wrapper for offline-first emergency guidance on smartphones
6. **Advanced mapping** — Folium/Plotly with real-time disaster polygon overlays and evacuation routes

---

## ⚠️ Disclaimer

This tool is for **information and coordination purposes only**. Always follow official emergency guidance and call emergency services when lives are at risk.

| Country | Emergency Number |
|---|---|
| 🇮🇳 India | 112 |
| 🇺🇸 USA | 911 |
| 🇪🇺 Europe | 112 |
| 🇬🇧 UK | 999 |
| 🇦🇺 Australia | 000 |
| 🇨🇦 Canada | 911 |

---

## 👤 Author

**Mokshit Sharma**
B.Tech + M.Tech (Dual Degree) — AI & Data Science | DAVV, Indore
📧 sharman48520@gmail.com | 🌐 [mokshitsharma27.vercel.app](https://mokshitsharma27.vercel.app)
🔗 [LinkedIn](https://linkedin.com/in/mokshit-sharma-75b5ab305) | 💻 [GitHub](https://github.com/Mokshitsharma)

---

⭐ Star this repo if you found it useful!
