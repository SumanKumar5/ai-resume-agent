import logging
from config import SIMILARITY_THRESHOLD

logger = logging.getLogger(__name__)


def extract_text_from_tailored(tailored: dict) -> str:
    parts = []
    parts.append(tailored.get("summary", ""))
    for exp in tailored.get("experience", []):
        parts.extend(exp.get("bullets", []))
    for project in tailored.get("projects", []):
        parts.extend(project.get("bullets", []))
    return " ".join(parts).lower()


def extract_text_from_original(resume_text: str) -> str:
    return resume_text.lower()


def compute_similarity(text1: str, text2: str) -> float:
    words1 = set(text1.split())
    words2 = set(text2.split())
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)


def validate_resume_quality(tailored: dict, original_resume_text: str, job_title: str) -> bool:
    tailored_text = extract_text_from_tailored(tailored)
    original_text = extract_text_from_original(original_resume_text)
    similarity = compute_similarity(tailored_text, original_text)
    logger.info(f"Resume similarity score for {job_title}: {similarity:.2f} (threshold: {SIMILARITY_THRESHOLD})")
    if similarity > SIMILARITY_THRESHOLD:
        logger.warning(f"Tailored resume for {job_title} is too similar to original (score: {similarity:.2f}). Consider improving the prompt.")
        return False
    logger.info(f"Resume quality check passed for {job_title}.")
    return True