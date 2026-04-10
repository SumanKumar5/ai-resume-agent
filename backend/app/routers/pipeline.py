import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.tasks import run_pipeline_task
from app.websocket_manager import manager
from celery.result import AsyncResult
import asyncio
import shutil
import os

router = APIRouter()


@router.post("/run")
async def run_pipeline(
    excel_file: UploadFile = File(None),
    json_file: UploadFile = File(None),
    resume_file: UploadFile = File(None),
    receiver_email: str = Form(None)
):
    excel_path = "inputs/option2_job_links.xlsx"
    json_path = "inputs/option2_jobs.json"
    resume_path = "inputs/candidate_resume.docx"

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    if excel_file and excel_file.filename:
        excel_path = f"{upload_dir}/{excel_file.filename}"
        with open(excel_path, "wb") as f:
            shutil.copyfileobj(excel_file.file, f)

    if json_file and json_file.filename:
        json_path = f"{upload_dir}/{json_file.filename}"
        with open(json_path, "wb") as f:
            shutil.copyfileobj(json_file.file, f)

    if resume_file and resume_file.filename:
        resume_path = f"{upload_dir}/{resume_file.filename}"
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(resume_file.file, f)

    task = run_pipeline_task.delay(
        excel_path=excel_path,
        json_path=json_path,
        resume_path=resume_path,
        receiver_email=receiver_email
    )

    return JSONResponse({"task_id": task.id})


@router.get("/task/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }


@router.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(task_id, websocket)
    last_log = None
    try:
        result = AsyncResult(task_id)
        while not result.ready():
            if result.state == "PROGRESS":
                meta = result.info or {}
                current_log = meta.get("log", "")
                if current_log and current_log != last_log:
                    await manager.broadcast(task_id, {
                        "log": current_log,
                        "level": meta.get("level", "info")
                    })
                    last_log = current_log
            await asyncio.sleep(0.5)
            result = AsyncResult(task_id)

        await manager.broadcast(task_id, {
            "log": "Pipeline finished.",
            "level": "success",
            "done": True,
            "result": result.result
        })
    except WebSocketDisconnect:
        manager.disconnect(task_id, websocket)