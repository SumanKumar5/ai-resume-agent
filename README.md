# AI Resume Tailoring Agent

An automated AI-powered pipeline that customizes a candidate’s resume for multiple job roles and delivers tailored applications via email.

---

## Overview

This project implements an **end-to-end intelligent agent** that:

* Reads job data from Excel + JSON
* Extracts candidate resume from `.docx`
* Uses AI (Google Gemini) to tailor resumes per job
* Generates customized resumes
* Sends each resume via email with job details

The system is fully automated, fault-tolerant, and modular.

---

## Tech Stack

* **Language:** Python
* **AI Model:** Google Gemini (gemini-1.5-flash)
* **Libraries:**

  * `openpyxl` – Excel parsing
  * `python-docx` – Resume reading/writing
  * `google-generativeai` – AI integration
  * `smtplib` – Email automation
  * `python-dotenv` – Environment variables

---

## Project Structure

```id="y3r1xg"
ai-resume-agent/
│
├── main.py
├── services/
│   ├── excel_reader.py
│   ├── llm_service.py
│   ├── resume_generator.py
│   ├── email_service.py
│
├── data/
│   ├── option2_job_links.xlsx
│   ├── option2_jobs.json
│   ├── candidate_resume.docx
│
├── output/
│   └── resumes/
│
├── .env
├── .env.example
├── README.md
```

---

## How It Works

```id="4blh42"
Excel + JSON → Merge → Read Resume → AI Tailoring → Generate Resume → Email भेजना
```

### Step-by-step flow:

1. Load job links from Excel
2. Load job descriptions from JSON
3. Merge both using job ID
4. Extract resume content from `.docx`
5. Send resume + job description to Gemini
6. Generate tailored resume
7. Save as `.docx`
8. Email resume + job details

---

## AI Prompt Strategy

The system uses structured prompts to ensure:

* Role-specific skill emphasis
* Resume summary customization
* Keyword alignment with job description
* No hallucinated experience

---

## Setup Instructions

### 1. Clone Repository

```bash id="s9gmbh"
git clone <your-repo-url>
cd ai-resume-agent
```

---

### 2. Create Virtual Environment

```bash id="dr1csi"
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash id="dnnvt6"
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create `.env`:

```env id="i0xzja"
GEMINI_API_KEY=your_api_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

---

### 5. Run Project

```bash id="0p8dd9"
python main.py
```

---

## Output

* 5 tailored resumes generated:

```id="fdqwdm"
output/resumes/
```

* 5 emails sent (one per job)

---

## Assumptions

* User has a valid Gemini API key
* Gmail App Password is configured
* Resume is in `.docx` format
* Internet connection is available

---

## Error Handling

* Each job processed independently
* API failures do not stop execution
* Email failures are logged and skipped
* File read/write errors handled gracefully

---


