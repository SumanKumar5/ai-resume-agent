import os
import sys
import time
import logging
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_admin.settings")
os.environ.setdefault("PYTHONPATH", str(Path(__file__).resolve().parent.parent))
django.setup()

from app.celery_app import celery_app
from django_admin.models import PipelineRun, JobResult
from modules.parser import load_all_inputs
from modules.llm import tailor_resume
from modules.docgen import generate_resume
from modules.emailer import send_resume_email
from modules.quality import validate_resume_quality
from config import RATE_LIMIT_DELAY, EXCEL_PATH, JSON_PATH, RESUME_PATH, OUTPUT_DIR

logger = logging.getLogger(__name__)


def push_log(task, message: str, level: str = "info"):
    task.update_state(
        state="PROGRESS",
        meta={"log": message, "level": level}
    )


@celery_app.task(bind=True, name="run_pipeline")
def run_pipeline_task(self, excel_path=None, json_path=None, resume_path=None, receiver_email=None):
    run = PipelineRun.objects.create(status="running", task_id=self.request.id)

    excel_path = excel_path or EXCEL_PATH
    json_path = json_path or JSON_PATH
    resume_path = resume_path or RESUME_PATH

    try:
        push_log(self, "Starting Resume Tailoring Pipeline...")
        jobs, resume_text = load_all_inputs(excel_path, json_path, resume_path)
        push_log(self, f"Loaded {len(jobs)} jobs successfully.")
        run.total_jobs = len(jobs)
        run.save()

        successful = 0
        failed = 0

        for i, job in enumerate(jobs):
            job_title = job["title"]
            company = job["company"]
            push_log(self, f"Processing job {i+1}/{len(jobs)}: {job_title}")

            job_result = JobResult.objects.create(
                run=run,
                job_title=job_title,
                company=company,
                status="processing"
            )

            start_time = time.time()

            try:
                push_log(self, f"Tailoring resume for {job_title}...")
                tailored_data = tailor_resume(job, resume_text)
                job_result.retries = 0

                similarity = validate_resume_quality(tailored_data, resume_text, job_title)
                job_result.similarity_score = similarity if isinstance(similarity, float) else None
                push_log(self, f"Quality check passed for {job_title}.")

            except Exception as e:
                push_log(self, f"LLM failed for {job_title}: {e}", "error")
                job_result.status = "failed"
                job_result.error = str(e)
                job_result.processing_time = time.time() - start_time
                job_result.save()
                failed += 1
                continue

            try:
                push_log(self, f"Generating PDF for {job_title}...")
                pdf_path = generate_resume(
                    data=tailored_data,
                    job_title=job_title,
                    candidate_name=tailored_data["name"],
                    output_dir=OUTPUT_DIR
                )
                job_result.pdf_path = pdf_path
                push_log(self, f"PDF saved: {pdf_path}")

            except Exception as e:
                push_log(self, f"PDF generation failed for {job_title}: {e}", "error")
                job_result.status = "failed"
                job_result.error = str(e)
                job_result.processing_time = time.time() - start_time
                job_result.save()
                failed += 1
                continue

            try:
                push_log(self, f"Sending email for {job_title}...")
                emailed = send_resume_email(job, pdf_path, receiver_email=receiver_email)
                job_result.email_status = emailed
                if emailed:
                    push_log(self, f"Email sent successfully for {job_title}.")
                else:
                    push_log(self, f"Email failed for {job_title}.", "warning")

            except Exception as e:
                push_log(self, f"Email error for {job_title}: {e}", "error")
                job_result.email_status = False

            job_result.status = "success" if job_result.email_status else "failed"
            job_result.processing_time = round(time.time() - start_time, 2)
            job_result.save()

            if job_result.status == "success":
                successful += 1
            else:
                failed += 1

            if i < len(jobs) - 1:
                push_log(self, f"Waiting {RATE_LIMIT_DELAY}s before next job...")
                time.sleep(RATE_LIMIT_DELAY)

        run.successful = successful
        run.failed = failed
        run.status = "completed"
        run.save()

        push_log(self, f"Pipeline complete. {successful}/{len(jobs)} resumes sent successfully.")
        return {"status": "completed", "successful": successful, "failed": failed}

    except Exception as e:
        run.status = "failed"
        run.save()
        push_log(self, f"Pipeline failed: {e}", "error")
        raise