from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pymupdf as fitz
import pytest

from doc2md_toolkit.cli import convert_one
from doc2md_toolkit.engines import markitdown_engine


def args() -> Namespace:
    return Namespace(engine="auto", vertical_text=False, format="md")


def test_named_teaching_pdf_uses_pdf2txt(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    src = tmp_path / "國語教材.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Lesson content")
    doc.save(src)

    dest = tmp_path / "out.md"
    convert_one(src, dest, args())

    assert "Lesson content" in dest.read_text(encoding="utf-8")
    assert "[完成] pdf2txt" in capsys.readouterr().out


def test_no_text_pdf_is_not_reported_as_success(tmp_path: Path) -> None:
    src = tmp_path / "blank.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(src)

    dest = tmp_path / "out.md"
    with pytest.raises(RuntimeError, match="找不到可擷取文字"):
        convert_one(src, dest, args())
    assert not dest.exists()


def test_conversion_never_overwrites_source(tmp_path: Path) -> None:
    src = tmp_path / "same.pdf"
    src.write_bytes(b"unchanged")
    with pytest.raises(RuntimeError, match="覆蓋原始檔"):
        convert_one(src, src, args())
    assert src.read_bytes() == b"unchanged"


def test_partial_text_pdf_marks_missing_page(tmp_path: Path) -> None:
    src = tmp_path / "lesson.pdf"
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "Page one")
    doc.new_page()
    doc.save(src)

    dest = tmp_path / "out.md"
    convert_one(src, dest, args())
    output = dest.read_text(encoding="utf-8")
    assert "PDF 第 2 頁沒有可擷取文字" in output
    assert "Page one" in output


def test_auto_pdf_falls_back_when_markitdown_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    src = tmp_path / "general.pdf"
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "Fallback content")
    doc.save(src)

    def fail_markitdown(_: Path) -> str:
        raise RuntimeError("converter failed")

    monkeypatch.setattr(markitdown_engine, "convert", fail_markitdown)
    dest = tmp_path / "out.md"
    convert_one(src, dest, args())
    assert "Fallback content" in dest.read_text(encoding="utf-8")
