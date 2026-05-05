from __future__ import annotations

from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".doc",
    ".pptx",
    ".ppt",
    ".xlsx",
    ".xls",
    ".html",
    ".htm",
    ".csv",
    ".json",
    ".xml",
    ".zip",
    ".epub",
    ".txt",
    ".md",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
}


def choose_engine(path: Path, requested: str, *, vertical_text: bool = False, ocr: bool = False) -> str:
    if requested != "auto":
        return requested

    suffix = path.suffix.lower()
    if ocr:
        return "mineru"
    if suffix == ".pdf" and vertical_text:
        return "pdf2txt"
    return "markitdown"


def iter_inputs(path: Path, recursive: bool = False) -> list[Path]:
    if path.is_file():
        return [path]
    pattern = "**/*" if recursive else "*"
    return sorted(p for p in path.glob(pattern) if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)
