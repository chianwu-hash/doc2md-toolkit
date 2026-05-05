from pathlib import Path

from doc2md_toolkit.detect import choose_engine


def test_choose_engine_defaults_to_markitdown() -> None:
    assert choose_engine(Path("file.docx"), "auto") == "markitdown"


def test_choose_engine_uses_pdf2txt_for_vertical_pdf() -> None:
    assert choose_engine(Path("textbook.pdf"), "auto", vertical_text=True) == "pdf2txt"


def test_choose_engine_uses_mineru_for_ocr() -> None:
    assert choose_engine(Path("scan.pdf"), "auto", ocr=True) == "mineru"
