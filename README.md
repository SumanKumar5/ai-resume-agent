<div align="center">

![AI Resume Agent Banner](https://img.shields.io/badge/AI%20Resume%20Tailoring%20Agent-v3.0.0-6366f1?style=for-the-badge&logoColor=white)

**A production-grade, full-stack AI agent that tailors resumes to job descriptions using NVIDIA NIM (Llama 3.3 70B) — with a real-time web dashboard, background task processing, and persistent analytics.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Celery](https://img.shields.io/badge/Celery-5.6-37814A?style=flat-square&logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io)
[![Vite](https://img.shields.io/badge/Vite-8.0-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.0-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA%20NIM-Llama%203.3%2070B-76B900?style=flat-square&logo=nvidia&logoColor=white)](https://build.nvidia.com/models)
[![SendGrid](https://img.shields.io/badge/SendGrid-API-1A82E2?style=flat-square&logo=twilio&logoColor=white)](https://sendgrid.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

<br/>

[Quick Start](#quick-start) · [Architecture](#architecture) · [API Docs](#api-documentation)

</div>

---

## Overview

The AI Resume Tailoring Agent is a fully autonomous pipeline that:

1. Reads a candidate's resume (`.docx` or `.pdf`) and a set of job descriptions
2. Uses **NVIDIA NIM (Llama 3.3 70B)** to uniquely tailor the resume for each role — rewriting the summary, reordering skills, and emphasizing relevant experience
3. Validates quality using a **Jaccard similarity score** to ensure each resume is meaningfully different from the original
4. Generates a professionally formatted **PDF** for each tailored resume
5. Delivers each resume via a **beautiful HTML email** through SendGrid
6. Logs everything to a **SQLite database** with a full-featured **Django Admin** panel
7. Streams real-time pipeline logs to the browser via **WebSockets**

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend (Vite)                  │
│         Run Pipeline │ History │ Analytics               │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP + WebSocket
┌──────────────────────▼──────────────────────────────────┐
│                   FastAPI Backend                        │
│    POST /api/run  │  GET /api/runs  │  WS /api/ws/{id}  │
└──────┬────────────────────────────────────┬─────────────┘
       │ dispatch task                       │ stream logs
┌──────▼──────────┐                ┌────────▼────────────┐
│  Celery Worker  │                │   Redis (broker +   │
│  (run_pipeline) │                │    result backend)  │
└──────┬──────────┘                └─────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────┐
│                  Pipeline Modules                        │
│  Parser → LLM (NVIDIA NIM) → Quality Check → DocGen → Email │
└──────┬──────────────────────────────────────────────────┘
       │ ORM writes
┌──────▼──────────────────────────────────────────────────┐
│              Django ORM + SQLite                         │
│         PipelineRun │ JobResult                         │
└──────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend

| Layer          | Technology                          |
| -------------- | ----------------------------------- |
| API Framework  | FastAPI 0.115                       |
| ASGI Server    | Uvicorn                             |
| Task Queue     | Celery 5.6                          |
| Message Broker | Redis 7 (Docker)                    |
| ORM            | Django 6.0 ORM                      |
| Admin Panel    | Django Admin                        |
| Database       | SQLite (dev) / PostgreSQL (prod)    |
| LLM            | NVIDIA NIM — Llama 3.3 70B Instruct |
| LLM SDK        | `openai` (OpenAI-compatible API)    |
| Email          | SendGrid API                        |
| Resume Input   | `python-docx` + `pdfplumber`        |
| Resume Output  | `python-docx` + `docx2pdf`          |
| Excel Parsing  | `openpyxl`                          |
| Validation     | Pydantic v2                         |
| WSGI Bridge    | `a2wsgi`                            |
| Config         | `python-dotenv`                     |

### Frontend

| Layer       | Technology           |
| ----------- | -------------------- |
| Framework   | React 18             |
| Build Tool  | Vite 8               |
| Styling     | TailwindCSS 4        |
| Charts      | Recharts             |
| Icons       | Lucide React         |
| Routing     | React Router v6      |
| HTTP Client | Axios                |
| Real-time   | Native WebSocket API |

---

## Project Structure

```
ai-resume-agent/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── celery_app.py
│   │   ├── tasks.py
│   │   ├── websocket_manager.py
│   │   └── routers/
│   │       ├── pipeline.py
│   │       ├── history.py
│   │       └── analytics.py
│   ├── django_admin/
│   │   ├── settings.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── migrations/
│   ├── modules/
│   │   ├── parser.py
│   │   ├── llm.py
│   │   ├── docgen.py
│   │   ├── emailer.py
│   │   ├── validator.py
│   │   └── quality.py
│   ├── inputs/
│   ├── outputs/
│   ├── logs/
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Run.jsx
│   │   │   ├── History.jsx
│   │   │   └── Analytics.jsx
│   │   ├── components/
│   │   │   └── Navbar.jsx
│   │   ├── lib/
│   │   │   └── api.js
│   │   └── App.jsx
│   ├── vite.config.js
│   └── package.json
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker Desktop (for Redis)
- Microsoft Word (required by `docx2pdf` on Windows)
- NVIDIA Developer account → [build.nvidia.com](https://build.nvidia.com/models)
- SendGrid account → [sendgrid.com](https://sendgrid.com)

---

### 1. Clone the Repository

```bash
git clone https://github.com/SumanKumar5/ai-resume-agent.git
cd ai-resume-agent
git checkout v3
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables

```bash
cp ../.env.example .env
```

Fill in `backend/.env`:

```env
NVIDIA_API_KEY=your_nvidia_nim_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=your_verified_sender@gmail.com
RECEIVER_EMAIL=default_receiver@gmail.com
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///db.sqlite3
DJANGO_SECRET_KEY=your_secret_key
```

**Getting your API keys:**

- **NVIDIA API key** → [build.nvidia.com/models](https://build.nvidia.com/models) → Sign in → Get API Key
- **SendGrid API key** → SendGrid Dashboard → Settings → API Keys → Create API Key (Full Access)
- **Verify sender email** → SendGrid Dashboard → Settings → Sender Authentication → Single Sender Verification

### 4. Database Setup

```bash
# Windows — set these in every new terminal
set PYTHONPATH=D:\path\to\ai-resume-agent\backend
set DJANGO_SETTINGS_MODULE=django_admin.settings

python django_admin/manage.py migrate
python django_admin/manage.py createsuperuser
```

### 5. Frontend Setup

```bash
cd ../frontend
npm install
```

### 6. Start All Services

You need **4 terminals** running simultaneously:

**Terminal 1 — Redis:**

```bash
docker run -d --name redis-resume -p 6379:6379 redis:latest
# or if already created:
docker start redis-resume
```

**Terminal 2 — FastAPI:**

```bash
cd backend
venv\Scripts\activate  # Windows
set PYTHONPATH=D:\path\to\ai-resume-agent\backend
set DJANGO_SETTINGS_MODULE=django_admin.settings
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 — Celery:**

```bash
cd backend
venv\Scripts\activate  # Windows
set PYTHONPATH=D:\path\to\ai-resume-agent\backend
set DJANGO_SETTINGS_MODULE=django_admin.settings
celery -A app.celery_app worker --loglevel=info --pool=solo
```

**Terminal 4 — React:**

```bash
cd frontend
npm run dev
```

### 7. Open the App

| Service           | URL                         |
| ----------------- | --------------------------- |
| React Dashboard   | http://localhost:5173       |
| FastAPI + Swagger | http://localhost:8000/docs  |
| Django Admin      | http://localhost:8000/admin |

---

## Usage

### Running the Pipeline

1. Go to **http://localhost:5173**
2. Upload your files (or leave empty to use defaults):
   - Job Links Excel (`.xlsx`) — columns: `#`, `Job Title`, `Company`, `URL`, `Resume Path`
   - Jobs JSON (`.json`) — array of job objects with `id`, `title`, `description`, `requirements`
   - Candidate Resume (`.docx` or `.pdf`)
3. Optionally enter a custom receiver email
4. Click **Run Pipeline**
5. Watch real-time logs stream in as each job is processed

### Input File Format

**Excel (`option2_job_links.xlsx`):**
| # | Job Title | Company | URL | Resume Path |
|---|---|---|---|---|
| 1 | Backend Engineer | Acme Corp | https://... | ./resume/candidate_resume.docx |

**JSON (`option2_jobs.json`):**

```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Backend Engineer",
      "company": "Acme Corp",
      "url": "https://...",
      "description": "We are looking for...",
      "requirements": ["Python", "FastAPI", "PostgreSQL"],
      "nice_to_have": ["Kubernetes", "AWS"]
    }
  ]
}
```

---

## API Documentation

FastAPI auto-generates interactive API docs at **http://localhost:8000/docs**

| Method | Endpoint                 | Description                                 |
| ------ | ------------------------ | ------------------------------------------- |
| `POST` | `/api/run`               | Trigger pipeline with optional file uploads |
| `GET`  | `/api/task/{task_id}`    | Get Celery task status                      |
| `WS`   | `/api/ws/{task_id}`      | WebSocket for real-time log streaming       |
| `GET`  | `/api/runs`              | Get all pipeline run history                |
| `GET`  | `/api/runs/{run_id}`     | Get specific run with job results           |
| `GET`  | `/api/download/{job_id}` | Download tailored PDF resume                |
| `GET`  | `/api/analytics`         | Get analytics data for dashboard            |

---

## Key Design Decisions

**NVIDIA NIM via OpenAI-compatible API** - NVIDIA NIM exposes an OpenAI-compatible `/v1/chat/completions` endpoint, making it trivial to swap models by changing a single config string. Llama 3.3 70B was chosen for its strong instruction-following, structured JSON output, and free tier availability.

**Structured JSON output from LLM** - Prompting Llama 3.3 70B to return a strict JSON schema ensures reliable parsing and consistent document generation regardless of model response variation.

**Per-job error isolation** - Each job is wrapped in its own try/except block inside the Celery task. A failure on any single job never stops the pipeline from processing the remaining ones.

**Exponential backoff on rate limits** - The LLM module retries up to 3 times with exponentially increasing delays (2s, 4s, 8s) when hitting rate limit or service unavailability errors.

**WebSocket log streaming** - Logs are pushed from the Celery worker via Redis task state updates, polled by FastAPI, and streamed to the browser — giving real-time visibility without blocking the UI.

**Django ORM alongside FastAPI** - Django is used purely for its ORM and Admin panel. FastAPI handles all API routing. The two are bridged via `a2wsgi`, a clean and well-documented pattern for running Django WSGI alongside FastAPI ASGI.

**Jaccard similarity quality gate** - After each LLM call, a similarity score between the tailored and original resume is computed. If the score exceeds 0.85, a warning is logged - ensuring each resume is meaningfully differentiated.

**Timestamped outputs** - Every PDF and log file is timestamped, so re-runs never overwrite previous results and every run is fully auditable.

---

## Assumptions

- Microsoft Word is installed on Windows machines (required by `docx2pdf`)
- The evaluator has a SendGrid account with a verified sender email
- The evaluator has an NVIDIA Developer account to generate a NIM API key
- Redis is available via Docker

---

## Environment Variables Reference

| Variable            | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| `NVIDIA_API_KEY`    | NVIDIA NIM API key from build.nvidia.com                   |
| `SENDGRID_API_KEY`  | SendGrid API key for email delivery                        |
| `SENDER_EMAIL`      | Verified sender email in SendGrid                          |
| `RECEIVER_EMAIL`    | Default receiver email (overridable in UI)                 |
| `REDIS_URL`         | Redis connection URL (default: `redis://localhost:6379/0`) |
| `DATABASE_URL`      | Database URL (default: SQLite)                             |
| `DJANGO_SECRET_KEY` | Django secret key                                          |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ using Python, FastAPI, React, Django, Celery, Redis, and NVIDIA NIM (Llama 3.3 70B)

**[ Back to top](#ai-resume-tailoring-agent)**

</div>
