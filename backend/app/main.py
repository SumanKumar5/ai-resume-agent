import os
import sys
import django
from pathlib import Path
from fastapi.staticfiles import StaticFiles

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_admin.settings")
os.environ.setdefault("PYTHONPATH", str(Path(__file__).resolve().parent.parent))
django.setup()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from a2wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application
from app.routers import pipeline, history, analytics

django_app = get_wsgi_application()

app = FastAPI(
    title="AI Resume Tailoring Agent",
    description="Production-grade AI pipeline for tailoring resumes to job descriptions.",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pipeline.router, prefix="/api", tags=["Pipeline"])
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])

app.mount("/admin", WSGIMiddleware(django_app), name="django_admin")
app.mount("/admin-static", StaticFiles(directory="staticfiles"), name="static")


@app.get("/")
def root():
    return {"message": "AI Resume Tailoring Agent v3.0.0", "status": "running"}