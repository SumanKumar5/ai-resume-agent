from fastapi import APIRouter
from django_admin.models import PipelineRun, JobResult
from django.db.models import Avg, Count

router = APIRouter()


@router.get("/analytics")
def get_analytics():
    total_runs = PipelineRun.objects.count()
    total_jobs = JobResult.objects.count()
    total_successful = JobResult.objects.filter(status="success").count()
    total_failed = JobResult.objects.filter(status="failed").count()
    avg_similarity = JobResult.objects.aggregate(avg=Avg("similarity_score"))["avg"]
    avg_processing_time = JobResult.objects.aggregate(avg=Avg("processing_time"))["avg"]

    runs_over_time = list(
        PipelineRun.objects.values("timestamp", "successful", "failed", "status")
        .order_by("timestamp")
    )
    for r in runs_over_time:
        r["timestamp"] = r["timestamp"].isoformat()

    role_stats = list(
        JobResult.objects.values("job_title")
        .annotate(
            count=Count("id"),
            avg_similarity=Avg("similarity_score"),
            avg_time=Avg("processing_time")
        )
        .order_by("job_title")
    )

    email_stats = {
        "sent": JobResult.objects.filter(email_status=True).count(),
        "failed": JobResult.objects.filter(email_status=False).count()
    }

    return {
        "summary": {
            "total_runs": total_runs,
            "total_jobs": total_jobs,
            "total_successful": total_successful,
            "total_failed": total_failed,
            "avg_similarity_score": round(avg_similarity, 3) if avg_similarity else 0,
            "avg_processing_time": round(avg_processing_time, 2) if avg_processing_time else 0
        },
        "runs_over_time": runs_over_time,
        "role_stats": role_stats,
        "email_stats": email_stats
    }