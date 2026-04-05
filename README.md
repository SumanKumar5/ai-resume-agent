
# AI Resume Tailoring Agent

An autonomous AI-powered agent that reads a candidate's resume and a set of job descriptions, tailors the resume for each role using Google Gemini, generates a professionally formatted PDF for each job, and delivers them via email — fully automated, end to end.

---

## How It Works

```
Excel + JSON + Resume
        ↓
   Input Parsing
        ↓
  Gemini 2.5 Flash
  (Resume Tailoring)
        ↓
 Quality Validation
        ↓
  PDF Generation
        ↓
  Email Delivery
  (via SendGrid)
        ↓
 run_summary.json
```

1. **Parser** reads and merges `option2_job_links.xlsx` and `option2_jobs.json` into 5 combined job records, then extracts the full resume text from `candidate_resume.docx`.
2. **Validator** runs pre-flight checks on all environment variables, input files, and Excel column structure before the pipeline starts.
3. **LLM** sends a structured prompt to Gemini 2.5 Flash for each job, instructing it to rewrite the summary, reorder skills, emphasize relevant experience, and return a clean JSON object. Includes retry logic with exponential backoff for rate limit handling.
4. **Quality Check** computes a similarity score between the tailored and original resume to ensure meaningful differentiation.
5. **DocGen** rebuilds the tailored resume as a formatted `.docx` and converts it to a timestamped PDF.
6. **Emailer** sends one HTML email per job via SendGrid with the PDF attached and full job details in the body.
7. **Orchestrator** runs the full pipeline with per-job error handling and saves a `run_summary.json` on completion.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| LLM | Google Gemini 2.5 Flash |
| SDK | `google-genai` |
| Excel Parsing | `openpyxl` |
| Resume Input | `python-docx` |
| Resume Output | `python-docx` + `docx2pdf` |
| Email Delivery | SendGrid API |
| Config & Secrets | `python-dotenv` |
| Logging | Python `logging` module |

---

## Project Structure

```
resume-tailoring-agent/
├── main.py                  # Pipeline orchestrator
├── config.py                # Centralized configuration
├── modules/
│   ├── __init__.py
│   ├── parser.py            # Excel, JSON, and resume parsing
│   ├── llm.py               # Gemini API calls and prompt engineering
│   ├── docgen.py            # DOCX and PDF generation
│   ├── emailer.py           # SendGrid HTML email delivery
│   ├── validator.py         # Pre-flight input and env validation
│   └── quality.py           # Resume similarity quality check
├── inputs/
│   ├── option2_job_links.xlsx
│   ├── option2_jobs.json
│   └── candidate_resume.docx
├── outputs/                 # Generated PDFs and run_summary.json
├── logs/                    # Timestamped log files per run
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.12+
- Microsoft Word installed (required by `docx2pdf` on Windows)
- A Google AI Studio account ([aistudio.google.com](https://aistudio.google.com))
- A SendGrid account ([sendgrid.com](https://sendgrid.com)) with a verified sender email

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-tailoring-agent.git
cd resume-tailoring-agent
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:

```env
GEMINI_API_KEY=your_gemini_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=your_verified_sender@gmail.com
RECEIVER_EMAIL=where_to_receive_resumes@gmail.com
```

**Getting your API keys:**
- **Gemini API key** → [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → Create API Key
- **SendGrid API key** → SendGrid Dashboard → Settings → API Keys → Create API Key (Full Access)
- **Verify sender email** → SendGrid Dashboard → Settings → Sender Authentication → Single Sender Verification

### 5. Add Input Files

Ensure the following files exist in the `inputs/` folder:

```
inputs/
├── option2_job_links.xlsx
├── option2_jobs.json
└── candidate_resume.docx
```

### 6. Run the Agent

```bash
python main.py
```

---

## Output

Each run produces:

- **5 tailored PDF resumes** in `outputs/` with timestamped filenames
  ```
  resume_alex_j_morgan_backend_software_engineer_20260405_232109.pdf
  resume_alex_j_morgan_frontend_engineer_20260405_232139.pdf
  ...
  ```
- **5 HTML emails** delivered to `RECEIVER_EMAIL` with the PDF attached
- **A run summary JSON file** in `outputs/`
  ```json
  {
    "run_timestamp": "2026-04-05T23:23:20",
    "total_jobs": 5,
    "successful": 5,
    "failed": 0,
    "results": [...]
  }
  ```
- **A timestamped log file** in `logs/`

---

## Key Design Decisions

**Structured JSON output from LLM** — Prompting Gemini to return a strict JSON schema ensures reliable parsing and consistent document generation regardless of model response variation.

**Per-job error isolation** — Each job is wrapped in its own try/except block inside the main loop. A failure on any single job never stops the pipeline from processing the remaining ones.

**Exponential backoff on rate limits** — The LLM module retries up to 3 times with exponentially increasing delays when hitting Gemini API rate limits, making the pipeline resilient to transient quota errors.

**Resume quality validation** — After each LLM call, a Jaccard similarity score is computed between the tailored and original resume. If the score exceeds 0.85, a warning is logged, ensuring each resume is meaningfully differentiated.

**Rate limiting between jobs** — A configurable delay between API calls prevents hitting per-minute quota limits when processing multiple jobs in sequence.

**Centralized config** — All constants, paths, model names, and thresholds live in `config.py`. No magic strings scattered across modules.

**Timestamped outputs** — Every PDF and log file is timestamped, so re-runs never overwrite previous results and every run is fully auditable.

---
