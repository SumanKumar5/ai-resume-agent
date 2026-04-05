import logging
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from config import SENDGRID_API_KEY, SENDER_EMAIL, RECEIVER_EMAIL

logger = logging.getLogger(__name__)


def build_html_body(job: dict) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      background-color: #f4f6f9;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 620px;
      margin: 40px auto;
      background-color: #ffffff;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    .header {{
      background: linear-gradient(135deg, #1a1a2e, #16213e);
      padding: 36px 40px;
      text-align: center;
    }}
    .header h1 {{
      color: #ffffff;
      font-size: 22px;
      margin: 0 0 6px 0;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .header p {{
      color: #a0aec0;
      font-size: 13px;
      margin: 0;
    }}
    .body {{
      padding: 36px 40px;
    }}
    .greeting {{
      font-size: 15px;
      color: #2d3748;
      margin-bottom: 20px;
    }}
    .card {{
      background-color: #f7fafc;
      border-left: 4px solid #4f46e5;
      border-radius: 6px;
      padding: 20px 24px;
      margin-bottom: 24px;
    }}
    .card h2 {{
      font-size: 16px;
      color: #1a202c;
      margin: 0 0 14px 0;
      font-weight: 600;
    }}
    .card table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .card table td {{
      font-size: 13px;
      padding: 5px 0;
      color: #4a5568;
      vertical-align: top;
    }}
    .card table td:first-child {{
      font-weight: 600;
      color: #2d3748;
      width: 110px;
    }}
    .card table td a {{
      color: #4f46e5;
      text-decoration: none;
    }}
    .attachment-note {{
      background-color: #ebf4ff;
      border-radius: 6px;
      padding: 14px 18px;
      font-size: 13px;
      color: #2b6cb0;
      margin-bottom: 24px;
    }}
    .footer {{
      text-align: center;
      padding: 20px 40px;
      background-color: #f7fafc;
      font-size: 11px;
      color: #a0aec0;
      border-top: 1px solid #e2e8f0;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Tailored Resume Submission</h1>
      <p>AI-Powered Resume Tailoring Agent</p>
    </div>
    <div class="body">
      <p class="greeting">Hello,</p>
      <p class="greeting">Please find attached a tailored resume prepared specifically for the following position:</p>
      <div class="card">
        <h2>Position Details</h2>
        <table>
          <tr>
            <td>Job Title</td>
            <td>{job['title']}</td>
          </tr>
          <tr>
            <td>Company</td>
            <td>{job['company']}</td>
          </tr>
          <tr>
            <td>Job URL</td>
            <td><a href="{job['URL']}">{job['URL']}</a></td>
          </tr>
        </table>
      </div>
      <div class="attachment-note">
        📎 The tailored resume PDF is attached to this email.
      </div>
      <p class="greeting">This resume has been customized using AI to highlight the most relevant skills, experience, and language that match this specific role.</p>
      <p class="greeting">Best regards,<br><strong>Alex J. Morgan</strong></p>
    </div>
    <div class="footer">
      This email was generated automatically by the AI Resume Tailoring Agent.
    </div>
  </div>
</body>
</html>
"""


def send_resume_email(job: dict, pdf_path: str) -> bool:
    try:
        subject = f"Tailored Resume — {job['title']} at {job['company']}"

        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=RECEIVER_EMAIL,
            subject=subject,
            html_content=build_html_body(job)
        )

        with open(pdf_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        filename = os.path.basename(pdf_path)

        attachment = Attachment(
            FileContent(encoded),
            FileName(filename),
            FileType("application/pdf"),
            Disposition("attachment")
        )
        message.attachment = attachment

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        logger.info(f"Email sent for {job['title']} — Status: {response.status_code}")
        return True

    except Exception as e:
        logger.error(f"Email failed for {job['title']}: {e}")
        return False