from __future__ import annotations

from pathlib import Path


def convert(src: Path) -> str:
    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise RuntimeError('MarkItDown is not installed. Install with `pip install "markitdown[all]"`.') from exc

    md = MarkItDown(enable_plugins=False)
    result = md.convert(str(src))
    return (result.text_content or "").strip()
