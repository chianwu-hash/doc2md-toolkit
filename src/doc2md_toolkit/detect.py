from __future__ import annotations

from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".xls",
    ".html",
    ".htm",
    ".csv",
    ".json",
    ".xml",
    ".zip",
    ".epub",
}

TEACHING_PDF_HINTS = (
    "教材",
    "教冊",
    "教師手冊",
    "教學篇",
    "備課",
    "課本",
    "習作",
    "國語",
    "數學",
    "自然",
    "textbook",
    "teacher-guide",
    "teacher_guide",
)


def choose_engine(path: Path, requested: str, *, vertical_text: bool = False) -> str:
    if requested != "auto":
        return requested

    suffix = path.suffix.lower()
    if suffix == ".pdf" and vertical_text:
        return "pdf2txt"
    if suffix == ".pdf" and any(hint in path.stem.casefold() for hint in TEACHING_PDF_HINTS):
        return "pdf2txt"
    return "markitdown"


def iter_inputs(path: Path, recursive: bool = False) -> list[Path]:
    if path.is_file():
        return [path]
    pattern = "**/*" if recursive else "*"
    return sorted(p for p in path.glob(pattern) if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)
