import logging
import json
import time
from google import genai
from google.genai.errors import ClientError
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_RETRIES, RETRY_BASE_DELAY

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)


def build_prompt(job: dict, resume_text: str) -> str:
    requirements = "\n".join(f"- {r}" for r in job.get("requirements", []))
    nice_to_have = "\n".join(f"- {n}" for n in job.get("nice_to_have", []))

    return f"""
You are an expert resume writer and career coach.

Your task is to tailor the candidate's resume specifically for the job below.
Return ONLY a valid JSON object. No markdown, no backticks, no explanation.

JOB DETAILS:
Title: {job['title']}
Company: {job['company']}
Description: {job['description']}

Required Skills:
{requirements}

Nice to Have:
{nice_to_have}

ORIGINAL RESUME:
{resume_text}

INSTRUCTIONS:
1. Rewrite the Professional Summary (4-5 sentences) to directly mirror the language and priorities of this specific job. Use exact keywords from the job description.
2. Reorder the Technical Skills section so the most relevant skills for this role appear first. Remove or deprioritize skills irrelevant to this role.
3. Rewrite AT LEAST 70% of bullet points in Work Experience to emphasize achievements most relevant to this role. Use action verbs and metrics that align with this job's priorities. Keep all facts accurate, do not invent anything.
4. Reorder Projects so the most relevant ones for this role appear first. Rewrite project bullets to highlight aspects most relevant to this role.
5. Keep Education and Certifications unchanged.
6. The tone should match the company culture: use enterprise/scalability language for backend/devops roles, creative/user-focused language for frontend roles, research/analytical language for ML roles.
7. Every section must feel like it was written specifically for this role — not a generic resume with a changed title.

Return this exact JSON structure:
{{
  "name": "candidate full name",
  "contact": "contact line as a single string",
  "summary": "rewritten professional summary",
  "skills": {{
    "Languages": "comma separated list",
    "Frameworks": "comma separated list",
    "Databases": "comma separated list",
    "Cloud & DevOps": "comma separated list",
    "ML / Data": "comma separated list",
    "Tools": "comma separated list"
  }},
  "experience": [
    {{
      "title": "job title",
      "company": "company name",
      "period": "date range",
      "bullets": ["bullet 1", "bullet 2", "bullet 3", "bullet 4"]
    }}
  ],
  "projects": [
    {{
      "name": "project name",
      "url": "project url",
      "bullets": ["bullet 1", "bullet 2", "bullet 3"]
    }}
  ],
  "education": {{
    "degree": "degree name",
    "university": "university name",
    "period": "date range",
    "gpa": "GPA string",
    "details": ["detail 1", "detail 2", "detail 3"]
  }},
  "certifications": ["cert 1", "cert 2", "cert 3", "cert 4"]
}}
"""


def tailor_resume(job: dict, resume_text: str) -> dict:
    attempt = 0
    last_error = None

    while attempt < MAX_RETRIES:
        try:
            prompt = build_prompt(job, resume_text)
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            raw = response.text.strip()

            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            tailored = json.loads(raw)
            logger.info(f"LLM tailoring successful for: {job['title']}")
            return tailored

        except Exception as e:
            error_str = str(e)
            if any(code in error_str for code in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]):
                wait = RETRY_BASE_DELAY ** (attempt + 1)
                logger.warning(f"Retryable error for {job['title']}. Retrying in {wait}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                attempt += 1
                last_error = e
            else:
                logger.error(f"LLM call failed for {job['title']}: {e}")
                raise

    raise RuntimeError(f"LLM failed after {MAX_RETRIES} attempts for {job['title']}: {last_error}")