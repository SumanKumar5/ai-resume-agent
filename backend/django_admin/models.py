from django.db import models


class PipelineRun(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    total_jobs = models.IntegerField(default=0)
    successful = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")
    task_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Run {self.id} — {self.timestamp} — {self.status}"


class JobResult(models.Model):
    run = models.ForeignKey(PipelineRun, on_delete=models.CASCADE, related_name="job_results")
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    similarity_score = models.FloatField(null=True, blank=True)
    pdf_path = models.CharField(max_length=500, blank=True, null=True)
    email_status = models.BooleanField(default=False)
    retries = models.IntegerField(default=0)
    processing_time = models.FloatField(null=True, blank=True)
    error = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.job_title} @ {self.company} — {self.status}"