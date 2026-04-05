import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from modules.parser import load_all_inputs
from modules.llm import tailor_resume
from modules.docgen import generate_resume
from modules.emailer import send_resume_email
from modules.validator import validate_all
from modules.quality import validate_resume_quality
from config import RATE_LIMIT_DELAY

load_dotenv()

Path("logs").mkdir(exist_ok=True)
log_filename = f"logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Resume Tailoring Agent")
    validate_all()

    jobs, resume_text = load_all_inputs(
        excel_path="inputs/option2_job_links.xlsx",
        json_path="inputs/option2_jobs.json",
        resume_path="inputs/candidate_resume.docx"
    )

    results = []

    for job in jobs:
        job_title = job["title"]
        logger.info(f"Processing: {job_title}")

        result = {"job": job_title, "tailored": False, "pdf": None, "emailed": False, "error": None}

        try:
            tailored_data = tailor_resume(job, resume_text)
            result["tailored"] = True
            validate_resume_quality(tailored_data, resume_text, job_title)
        except Exception as e:
            result["error"] = f"LLM failed: {e}"
            logger.error(f"Skipping {job_title} due to LLM error: {e}")
            results.append(result)
            continue

        try:
            pdf_path = generate_resume(
                data=tailored_data,
                job_title=job_title,
                candidate_name=tailored_data["name"],
                output_dir="outputs"
            )
            result["pdf"] = pdf_path
        except Exception as e:
            result["error"] = f"Document generation failed: {e}"
            logger.error(f"Skipping email for {job_title} due to docgen error: {e}")
            results.append(result)
            continue

        try:
            emailed = send_resume_email(job, pdf_path)
            result["emailed"] = emailed
        except Exception as e:
            result["error"] = f"Email failed: {e}"
            logger.error(f"Email error for {job_title}: {e}")

        results.append(result)

        if job != jobs[-1]:
            logger.info(f"Waiting {RATE_LIMIT_DELAY}s before next job...")
            time.sleep(RATE_LIMIT_DELAY)

    logger.info("=" * 60)
    logger.info("FINAL SUMMARY")
    logger.info("=" * 60)

    success = [r for r in results if r["emailed"]]
    failed = [r for r in results if not r["emailed"]]

    for r in success:
        logger.info(f"✅ {r['job']} — PDF: {r['pdf']}")

    for r in failed:
        logger.error(f"❌ {r['job']} — Error: {r['error']}")

    logger.info(f"Done. {len(success)}/{len(jobs)} resumes sent successfully.")

    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total_jobs": len(jobs),
        "successful": len(success),
        "failed": len(failed),
        "results": results
    }

    summary_path = os.path.join("outputs", f"run_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Run summary saved: {summary_path}")


if __name__ == "__main__":
    main()