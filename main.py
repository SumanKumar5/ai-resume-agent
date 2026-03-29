from services.excel_reader import read_excel, read_json, merge_jobs
from services.resume_generator import read_resume, save_resume
from services.llm_service import generate_tailored_resume
from services.email_service import send_email


def main():
    excel_path = "data/option2_job_links.xlsx"
    json_path = "data/option2_jobs.json"
    resume_path = "data/candidate_resume.docx"

    excel_jobs = read_excel(excel_path)
    json_jobs = read_json(json_path)

    print("JSON DATA:\n", json_jobs)
    print("=" * 60)

    merged_jobs = merge_jobs(excel_jobs, json_jobs)

    print("\nMerged Jobs:\n")

    if not merged_jobs:
        print("[WARNING] No jobs merged. Check input files.")
        return

    for job in merged_jobs:
        print(f"ID: {job['id']}")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"URL: {job['url']}")
        print(f"Description: {job['description'][:100]}...")
        print("-" * 60)

    resume_text = read_resume(resume_path)

    if not resume_text:
        print("[ERROR] Resume could not be read.")
        return

    print("\nRESUME PREVIEW:\n")
    print(resume_text[:500])
    print("=" * 60)

    print("\nGENERATING + SENDING RESUMES...\n")

    for job in merged_jobs:
        try:
            print(f"Processing: {job['title']}")

            tailored_resume = generate_tailored_resume(resume_text, job)

            if not tailored_resume:
                print("[ERROR] Skipping due to AI failure\n")
                continue

            file_path = save_resume(tailored_resume, job)

            if not file_path:
                print("[ERROR] Skipping email due to save failure\n")
                continue

            send_email(job, file_path)

            print("-" * 60)

        except Exception as e:
            print(f"[ERROR] Failed for job {job['id']}: {e}\n")

    print("\n All jobs processed successfully.\n")


if __name__ == "__main__":
    main()