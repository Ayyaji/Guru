# GURU — Personal AI Operating Layer

Built by **Raghava S. Ayyaji** — a hands-on fullstack + AI systems learning project.

GURU isn't a chatbot. It's an orchestrator — a personal AI that talks like a human,
remembers conversations, and takes real actions across connected services (starting
with Gmail, more peripherals planned).

## Architecture
- **GURU** (`main.py`) decides what to do and owns all database writes
- **extract.py** is a separate LLM call that reads GURU's natural response and extracts
  structured intent (action, params) as JSON — no hardcoded keyword matching
- **Peripherals** (`gmail.py`) execute the actual action and report success/failure
- **Database** is relational — `history` (chat log) and `emails` (transaction log),
  linked by foreign key, not duplicated

This mirrors the multi-agent + judgment-layer pattern from CodeLens AI — a router/orchestrator
that decides, and specialized workers that execute.

## What it does
- Natural conversation powered by Groq (llama-3.3-70b-versatile)
- Reads and sends real Gmail — triggered by plain English, not commands
- Persists full chat history in SQLite with proper schema (PK/FK relationships)
- PDF upload and Q&A
- Clean dark-themed chat UI — built in vanilla HTML/CSS/JS, no frameworks

## Stack
| Layer | Tech |
|-------|------|
| Backend | FastAPI, Python |
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Database | SQLite (relational schema) |
| AI | Groq (llama-3.3-70b-versatile) |
| Email | Gmail API (OAuth2) |

## Run locally
```bash
# Backend
python backend/main.py

# Frontend (separate terminal)
cd frontend
python -m http.server 3000
```
Open `http://localhost:3000`

## Database schema
**history** — `id (PK), role, message, time`
**emails** — `id (PK), chat_id (FK → history.id), to_address, subject, body, status, time`

## What I learned building this
- REST APIs with FastAPI
- DOM manipulation, fetch API, async/await in vanilla JS
- SQL from scratch — CREATE, INSERT, SELECT, UPDATE, DELETE, indexes, foreign keys, normalization
- OAuth2 flow with Google APIs
- Separating orchestration from execution — same pattern as multi-agent systems
- Why hallucination happens when system prompts conflict with architecture

## Roadmap
- [ ] Wire chat_id through to emails table (in progress)
- [ ] Email format validation
- [ ] Scroll-to-load older messages (pagination)
- [ ] WhatsApp / Twitter peripherals
- [ ] Migrate to NoSQL for push-based peripheral updates
- [ ] React frontend rebuild
