# 🧭 AI-Powered Travel Assistant — Multi-Agent System (Agentic AI)

An end-to-end multi-agent travel planning assistant built with **LangGraph**, orchestrating specialized agents through a shared state graph to deliver real-time, personalized, and voice-enabled travel recommendations — fully grounded in live external data.

---

## 🚀 Overview

This project demonstrates a production-style **agentic AI architecture** where 7 specialized agents collaborate through a shared `TravelState` object to plan trips end-to-end — from weather-based destination filtering to budget-aware hotel recommendations — with built-in fault tolerance, persistent personalization, and secure authentication.

Instead of relying on an LLM to "guess" travel details, every recommendation is grounded in **live API data**, minimizing hallucination and maximizing real-world reliability.

---

## ✨ Key Features

- **Multi-Agent Orchestration** — 7 specialized agents (Weather, Attractions, Hotel, Memory, Budget, Personalization, Fallback) coordinated via LangGraph `StateGraph` with conditional edge routing.
- **Fault-Tolerant Execution** — Dynamically reroutes the graph when no climate-matched destinations are found, instead of failing outright.
- **Live API Grounding** — Integrates Open-Meteo (weather), OpenTripMap (points of interest), and Amadeus sandbox (hotels) to ground every recommendation in real-time data.
- **Dual-Memory Personalization** — Combines short-term, per-request `TravelState` with long-term `travel_history` / `search_history` tables (MySQL + SQLAlchemy) for persistent, cross-session personalization.
- **Secure, Stateless Auth** — JWT-based authentication (HS256, `python-jose`) with `passlib`/`bcrypt` password hashing, integrated directly into the LangGraph state via decoded `user_id` claims.
- **Voice-Driven Interaction** — End-to-end voice conversational flow using `SpeechRecognition` (STT) and `pyttsx3` (offline TTS).
- **Resilience & Observability** — Retry logic with graceful degradation on all external API calls, plus full LangSmith tracing of per-node inputs/outputs across the graph.

---

## 🏗️ Architecture

```
                ┌─────────────────────┐
                │   User Query/Voice  │
                └──────────┬──────────┘
                           │
                  ┌────────▼─────────┐
                  │   Auth (JWT)      │
                  └────────┬─────────┘
                           │
                  ┌────────▼─────────┐
                  │   TravelState     │  ← shared state object
                  └────────┬─────────┘
        ┌──────────┬───────┼───────┬──────────┐
        ▼          ▼       ▼       ▼          ▼
   ┌────────┐ ┌─────────┐ ┌─────┐ ┌────────┐ ┌──────────────┐
   │Weather │ │Attraction│ │Hotel│ │ Budget │ │Personalization│
   │ Agent  │ │  Agent   │ │Agent│ │ Agent  │ │    Agent      │
   └───┬────┘ └────┬─────┘ └──┬──┘ └───┬────┘ └──────┬───────┘
       │           │          │        │             │
       └─────┬─────┴────┬─────┴────┬───┴─────────────┘
             ▼           ▼          ▼
        ┌─────────┐  ┌────────┐ ┌──────────┐
        │ Memory  │  │Fallback│ │  Final    │
        │ Agent   │  │ Agent  │ │ Response  │
        └─────────┘  └────────┘ └──────────┘
```

Conditional edges allow the graph to reroute (e.g., to the Fallback Agent) when an agent cannot satisfy the query — such as no destinations matching a requested climate.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph (StateGraph), LangChain |
| LLM | Gemini API |
| Backend | FastAPI, Uvicorn |
| Database | MySQL, SQLAlchemy |
| Auth | JWT (`python-jose`, HS256), `passlib`, `bcrypt`, FastAPI `OAuth2PasswordBearer` |
| External APIs | Open-Meteo, OpenTripMap, weather |
| Voice | `SpeechRecognition` (STT), `pyttsx3` (TTS) |
| Observability | LangSmith |
| Language | Python |

---

## 📂 Agents

| Agent | Responsibility |
|---|---|
| **Weather Agent** | Filters destinations by real-time temperature/climate match via Open-Meteo |
| **Attractions Agent** | Two-step radius + detail fetch pipeline for POI discovery via OpenTripMap |
| **Hotel Agent** | Budget-aware hotel recommendations via Amadeus sandbox |
| **Budget Agent** | Validates and constrains recommendations against user budget |
| **Personalization Agent** | Injects past trip ratings, climate preferences, and budget history into LLM prompts |
| **Memory Agent** | Reads/writes long-term `travel_history` and `search_history` (MySQL) |
| **Fallback Agent** | Handles failure cases — e.g., no climate match found — by rerouting execution |

---

## 🔐 Authentication Flow

1. User logs in → password verified via `bcrypt`/`passlib`
2. JWT issued (`python-jose`, HS256)
3. Token validated on each request via FastAPI `OAuth2PasswordBearer`
4. Decoded `user_id` injected directly into the LangGraph `TravelState` — binding auth to the agent workflow without extra DB lookups

---

## 🎙️ Voice Interaction

- **Speech-to-Text**: Captures user queries via `SpeechRecognition`
- **Text-to-Speech**: Responds via offline `pyttsx3` synthesis
- Fully integrated into the same FastAPI backend as the text-based flow

---

## 🧱 Resilience & Observability

- **Retry logic** with graceful degradation on every external API call (weather, attractions, hotels)
- **LangSmith tracing** captures per-node inputs/outputs across the full graph execution, enabling debugging of exactly which agent/state failed and why

---

## 📦 Project Structure (suggested)

```
travelling-assistant/
├── agents/
│   ├── weather_agent.py
│   ├── attractions_agent.py
│   ├── hotel_agent.py
│   ├── budget_agent.py
│   ├── personalization_agent.py
│   ├── memory_agent.py
│   └── fallback_agent.py
├── auth/
│   └── jwt_handler.py
├── voice/
│   ├── stt.py
│   └── tts.py
├── db/
│   └── models.py
├── travelling_assistant.py     # Main LangGraph orchestration + FastAPI app
├── requirements.txt
└── README.md
```

> Adjust this section to match your actual repo structure.

---

## ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/Vivek-Kumar76/AI-powered-travelling-assistant-agentic-AI-.git
cd AI-powered-travelling-assistant-agentic-AI-

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# GEMINI_API_KEY, OPENTRIPMAP_API_KEY, AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET,
# MYSQL_CONNECTION_STRING, JWT_SECRET_KEY

# Run the FastAPI server
uvicorn travelling_assistant:app --reload
```

---

## 🌱 Future Improvements

- Add caching layer for frequently requested weather/attraction queries
- Extend Fallback Agent with multi-tier relaxation strategies (e.g., widen climate range before giving up)
- Add a lightweight frontend (React) for live demo purposes
- Containerize with Docker for easier deployment

---

## 👤 Author

**Vivek Kumar**
B.S. Computer Science & Data Analytics, IIT Patna
[GitHub](https://github.com/Vivek-Kumar76) · [LinkedIn](https://www.linkedin.com/in/vivek-kumar-2098a8371)
