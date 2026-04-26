import os
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "meta/llama-3.3-70b-instruct"
MAX_RETRIES = 3
RETRY_BASE_DELAY = 2

RATE_LIMIT_DELAY = 5

EXCEL_PATH = "inputs/option2_job_links.xlsx"
JSON_PATH = "inputs/option2_jobs.json"
RESUME_PATH = "inputs/candidate_resume.docx"
OUTPUT_DIR = "outputs"
LOG_DIR = "logs"

REQUIRED_EXCEL_COLUMNS = ["#", "Job Title", "Company", "URL", "Resume Path"]
REQUIRED_ENV_VARS = ["NVIDIA_API_KEY",
                     "SENDGRID_API_KEY", "SENDER_EMAIL", "RECEIVER_EMAIL"]

SIMILARITY_THRESHOLD = 0.85

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DJANGO_SETTINGS_MODULE = "django_admin.settings"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
