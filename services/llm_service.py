import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=api_key)


def generate_tailored_resume(resume_text, job):
    """
    Calls Gemini API to tailor resume for a specific job.
    """
    try:
        configure_gemini()

        model = genai.GenerativeModel("gemini-3-flash-preview")

        prompt = f"""
You are a professional resume optimizer.

TASK:
Tailor the given resume for the job below.

IMPORTANT RULES:
- Highlight relevant skills based on job
- Modify summary to match role
- Reorder experience if needed
- Use keywords from job description
- Keep it concise and professional
- DO NOT add fake experience

RESUME:
{resume_text}

JOB TITLE:
{job['title']}

COMPANY:
{job['company']}

JOB DESCRIPTION:
{job['description']}
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print(f"[ERROR] Gemini API failed: {e}")
        return None