from __future__ import annotations

from pathlib import Path


def convert(src: Path) -> str:
    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise RuntimeError('尚未安裝 MarkItDown。請在專案根目錄執行 `pip install -e ".[all]"`。') from exc

    md = MarkItDown(enable_plugins=False)
    result = md.convert(str(src))
    return (result.text_content or "").strip()
