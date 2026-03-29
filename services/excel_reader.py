import openpyxl
import json


def read_excel(file_path):
    """
    Reads Excel file and extracts job IDs and URLs.
    """
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        jobs = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            job_id = row[0]   
            url = row[3]      

            if job_id and url:
                jobs.append({
                    "id": job_id,
                    "url": url
                })

        return jobs

    except Exception as e:
        print(f"[ERROR] Failed to read Excel file: {e}")
        return []


def read_json(file_path):
    """
    Reads JSON file and extracts job list correctly.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, dict) and "jobs" in data:
                return data["jobs"]

            return data

    except Exception as e:
        print(f"[ERROR] Failed to read JSON file: {e}")
        return []


def merge_jobs(excel_jobs, json_jobs):
    """
    Merges Excel and JSON data using job ID.
    """
    try:
        json_map = {}

        # Build JSON lookup map safely
        for job in json_jobs:
            if isinstance(job, dict) and "id" in job:
                json_map[job["id"]] = job
            else:
                print(f"[WARNING] Skipping invalid JSON entry: {job}")

        merged = []

        for job in excel_jobs:
            job_id = job["id"]

            if job_id in json_map:
                j = json_map[job_id]

                combined = {
                    "id": job_id,
                    "url": job["url"],
                    "title": j.get("title"),
                    "company": j.get("company"),
                    "description": j.get("description"),
                }

                merged.append(combined)
            else:
                print(f"[WARNING] Job ID {job_id} not found in JSON")

        return merged

    except Exception as e:
        print(f"[ERROR] Failed to merge job data: {e}")
        return []