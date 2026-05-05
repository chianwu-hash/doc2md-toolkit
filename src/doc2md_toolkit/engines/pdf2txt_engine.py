from __future__ import annotations

from pathlib import Path


def looks_like_single_char_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and len(stripped) == 1


def normalize_vertical_text(text: str, min_run: int = 4) -> str:
    """Join likely vertical-text runs and remove control characters."""
    text = "".join(ch for ch in text if ch in "\n\t" or ord(ch) >= 32)
    lines = text.splitlines()
    out: list[str] = []
    run: list[str] = []

    def flush_run(force_join: bool = False) -> None:
        nonlocal run
        if not run:
            return
        if force_join or len(run) >= min_run:
            out.append("".join(part.strip() for part in run))
        else:
            out.extend(run)
        run = []

    for idx, line in enumerate(lines):
        if looks_like_single_char_line(line):
            run.append(line)
            continue

        prev_is_blank = bool(out) and out[-1] == ""
        next_line = lines[idx + 1] if idx + 1 < len(lines) else ""
        next_is_blank = not next_line.strip()
        force_join = len(run) >= 2 and (prev_is_blank or next_is_blank)
        flush_run(force_join=force_join)
        out.append(line)

    flush_run()

    cleaned: list[str] = []
    blank_count = 0
    for line in out:
        if line.strip():
            blank_count = 0
            cleaned.append(line.rstrip())
        else:
            blank_count += 1
            if blank_count <= 1:
                cleaned.append("")

    return "\n".join(cleaned).strip()


def convert(src: Path, output_format: str = "md") -> str:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is not installed. Install with `pip install PyMuPDF`.") from exc

    doc = fitz.open(src)
    chunks: list[str] = []
    for index, page in enumerate(doc, start=1):
        normalized = normalize_vertical_text(page.get_text())
        if output_format == "md":
            chunks.append(f"## Page {index}\n\n{normalized}".strip())
        else:
            chunks.append(f"=== Page {index} ===\n{normalized}".strip())
    return "\n\n".join(chunks).strip()
