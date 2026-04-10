from django.contrib import admin
from .models import PipelineRun, JobResult


class JobResultInline(admin.TabularInline):
    model = JobResult
    extra = 0
    readonly_fields = [
        "job_title", "company", "similarity_score",
        "pdf_path", "email_status", "retries",
        "processing_time", "error", "status"
    ]


@admin.register(PipelineRun)
class PipelineRunAdmin(admin.ModelAdmin):
    list_display = ["id", "timestamp", "status", "total_jobs", "successful", "failed", "task_id"]
    list_filter = ["status"]
    search_fields = ["task_id"]
    readonly_fields = ["timestamp", "task_id"]
    inlines = [JobResultInline]


@admin.register(JobResult)
class JobResultAdmin(admin.ModelAdmin):
    list_display = ["id", "run", "job_title", "company", "status", "email_status", "similarity_score", "processing_time"]
    list_filter = ["status", "email_status"]
    search_fields = ["job_title", "company"]
    readonly_fields = ["run", "job_title", "company", "similarity_score", "pdf_path", "email_status", "retries", "processing_time", "error", "status"]