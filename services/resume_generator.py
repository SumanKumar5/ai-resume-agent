from docx import Document
import os


def read_resume(file_path):
    """
    Reads a .docx resume and returns full text.
    """
    try:
        doc = Document(file_path)

        full_text = []

        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                full_text.append(text)

        return "\n".join(full_text)

    except Exception as e:
        print(f"[ERROR] Failed to read resume: {e}")
        return ""


def save_resume(text, job, output_dir="output/resumes"):
    """
    Saves tailored resume as a .docx file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Clean filename
        title = job["title"].replace(" ", "_").replace("/", "").lower()
        filename = f"resume_{title}.docx"
        file_path = os.path.join(output_dir, filename)

        doc = Document()

        for line in text.split("\n"):
            doc.add_paragraph(line)

        doc.save(file_path)

        print(f"[SUCCESS] Resume saved: {file_path}")

        return file_path

    except Exception as e:
        print(f"[ERROR] Failed to save resume: {e}")
        return None