import os
import logging
import openpyxl
from config import (
    REQUIRED_ENV_VARS,
    REQUIRED_EXCEL_COLUMNS,
    EXCEL_PATH,
    JSON_PATH,
    RESUME_PATH
)

logger = logging.getLogger(__name__)


def validate_env_vars():
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}")
    logger.info("Environment variables validated.")


def validate_input_files():
    for path in [EXCEL_PATH, JSON_PATH, RESUME_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required input file not found: {path}")
    logger.info("Input files validated.")


def validate_excel_columns():
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    missing = [col for col in REQUIRED_EXCEL_COLUMNS if col not in headers]
    if missing:
        raise ValueError(
            f"Missing required Excel columns: {', '.join(missing)}")
    logger.info("Excel columns validated.")


def validate_all():
    logger.info("Running pre-flight validation...")
    validate_env_vars()
    validate_input_files()
    validate_excel_columns()
    logger.info("All validations passed. Starting pipeline.")
