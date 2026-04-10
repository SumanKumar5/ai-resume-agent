from fastapi import APIRouter
from fastapi.responses import FileResponse
from django_admin.models import PipelineRun, JobResult
import os

router = APIRouter()


@router.get("/runs")
def get_runs():
    runs = PipelineRun.objects.prefetch_related("job_results").order_by("-timestamp")
    result = []
    for run in runs:
        result.append({
            "id": run.id,
            "timestamp": run.timestamp.isoformat(),
            "status": run.status,
            "total_jobs": run.total_jobs,
            "successful": run.successful,
            "failed": run.failed,
            "task_id": run.task_id,
            "jobs": [
                {
                    "id": jr.id,
                    "job_title": jr.job_title,
                    "company": jr.company,
                    "status": jr.status,
                    "email_status": jr.email_status,
                    "similarity_score": jr.similarity_score,
                    "processing_time": jr.processing_time,
                    "pdf_path": jr.pdf_path,
                    "error": jr.error
                }
                for jr in run.job_results.all()
            ]
        })
    return result


@router.get("/runs/{run_id}")
def get_run(run_id: int):
    try:
        run = PipelineRun.objects.prefetch_related("job_results").get(id=run_id)
        return {
            "id": run.id,
            "timestamp": run.timestamp.isoformat(),
            "status": run.status,
            "total_jobs": run.total_jobs,
            "successful": run.successful,
            "failed": run.failed,
            "task_id": run.task_id,
            "jobs": [
                {
                    "id": jr.id,
                    "job_title": jr.job_title,
                    "company": jr.company,
                    "status": jr.status,
                    "email_status": jr.email_status,
                    "similarity_score": jr.similarity_score,
                    "processing_time": jr.processing_time,
                    "pdf_path": jr.pdf_path,
                    "error": jr.error
                }
                for jr in run.job_results.all()
            ]
        }
    except PipelineRun.DoesNotExist:
        return {"error": "Run not found"}


@router.get("/download/{job_id}")
def download_pdf(job_id: int):
    try:
        jr = JobResult.objects.get(id=job_id)
        if jr.pdf_path and os.path.exists(jr.pdf_path):
            return FileResponse(
                jr.pdf_path,
                media_type="application/pdf",
                filename=os.path.basename(jr.pdf_path)
            )
        return {"error": "PDF not found"}
    except JobResult.DoesNotExist:
        return {"error": "Job result not found"}