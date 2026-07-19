from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import UploadFile

from app.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".markdown"}


def validate_upload_file(file: UploadFile) -> None:
    if not file.filename:
        raise ValueError("Uploaded file must have a filename.")

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"Unsupported file type. Allowed types: {allowed}")


def save_upload_file(file: UploadFile) -> Path:
    validate_upload_file(file)

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    original_filename = Path(file.filename).name
    file_extension = Path(original_filename).suffix.lower()
    stored_filename = f"{uuid4().hex}{file_extension}"

    file_path = upload_dir / stored_filename

    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024
    total_size = 0

    with file_path.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            total_size += len(chunk)

            if total_size > max_size_bytes:
                file_path.unlink(missing_ok=True)
                raise ValueError(
                    f"File too large. Maximum size is {settings.max_upload_size_mb} MB."
                )

            buffer.write(chunk)

    return file_path,original_filename