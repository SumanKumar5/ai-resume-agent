import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(job, file_path):
    """
    Sends email with resume attachment.
    """
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")

        if not email_user or not email_pass:
            raise ValueError("Email credentials not set in .env")

        msg = EmailMessage()
        msg["Subject"] = f"Application for {job['title']} - {job['company']}"
        msg["From"] = email_user
        msg["To"] = email_user 

        body = f"""
Hello,

Please find attached my tailored resume for the position below:

Job Title: {job['title']}
Company: {job['company']}
Job URL: {job['url']}

Thank you for your time and consideration.

Best regards,
Your Name
"""

        msg.set_content(body)

        with open(file_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)

        msg.add_attachment(file_data,
                           maintype="application",
                           subtype="octet-stream",
                           filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)

        print(f"[SUCCESS] Email sent for {job['title']}")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")