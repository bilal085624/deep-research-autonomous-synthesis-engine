# Deep Research Autonomous Synthesis Engine 🧠

A production-grade AI orchestration loop built with **LangGraph** and **Streamlit**. This engine utilizes a cyclic state machine to autonomously reason, search the web, and synthesize highly technical reports with verified citations.

## 🚀 Key Features
- **Cyclic State Machine:** Powered by LangGraph for multi-pass, deterministic node routing.
- **Durable Checkpointing:** Utilizes `MemorySaver` to maintain conversational context and session persistence.
- **Autonomous Tool Execution:** Integrates Tavily for real-time web scraping when the reasoning model determines context is insufficient.
- **Production-Ready Resiliency:** Implements exponential backoff and retry logic (`Tenacity`) to gracefully bypass API rate limits (e.g., 503 and 429 errors).

## 🛠️ Tech Stack
- **Orchestration:** LangGraph (v1.2.11) 
- **Reasoning Models:** Google Gemini (via `langchain-google-genai`)
- **Search Integration:** Tavily (via `langchain-tavily`)
- **Frontend UI:** Streamlit
- **Data Validation:** Pydantic

## ⚙️ Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/bilal085624/deep-research-autonomous-synthesis-engine.git](https://github.com/bilal085624/deep-research-autonomous-synthesis-engine.git)
   cd deep-research-autonomous-synthesis-engine