import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

GEMINI_MODEL = "gemini-2.5-flash"
MAX_RETRIES = 3
RETRY_BASE_DELAY = 2

RATE_LIMIT_DELAY = 5

EXCEL_PATH = "inputs/option2_job_links.xlsx"
JSON_PATH = "inputs/option2_jobs.json"
RESUME_PATH = "inputs/candidate_resume.docx"
OUTPUT_DIR = "outputs"
LOG_DIR = "logs"

REQUIRED_EXCEL_COLUMNS = ["#", "Job Title", "Company", "URL", "Resume Path"]
REQUIRED_ENV_VARS = ["GEMINI_API_KEY", "SENDGRID_API_KEY", "SENDER_EMAIL", "RECEIVER_EMAIL"]

SIMILARITY_THRESHOLD = 0.85