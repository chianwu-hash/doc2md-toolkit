from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .detect import choose_engine, iter_inputs
from .engines import markitdown_engine, pdf2txt_engine


def output_path_for(src: Path, output: Path | None, *, input_is_dir: bool, output_format: str) -> Path:
    suffix = ".txt" if output_format == "txt" else ".md"
    if output is None:
        return src.with_suffix(suffix)
    if input_is_dir or output.is_dir() or str(output).endswith(("/", "\\")):
        return output / src.with_suffix(suffix).name
    return output


def write_text(dest: Path, text: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text.rstrip() + "\n", encoding="utf-8")


def convert_one(src: Path, dest: Path, args: argparse.Namespace) -> None:
    if src.resolve() == dest.resolve():
        raise RuntimeError(f"輸出路徑會覆蓋原始檔：{src}")
    engine = choose_engine(src, args.engine, vertical_text=args.vertical_text)
    missing_pages: list[int] = []
    if src.suffix.lower() == ".pdf":
        readable_pages, missing_pages = pdf2txt_engine.text_layer_pages(src)
        if not readable_pages:
            raise RuntimeError(f"找不到可擷取文字：{src}。這可能是掃描或圖片型 PDF；請先使用 OCR 或查看原始頁面。")

    if engine == "markitdown":
        try:
            text = markitdown_engine.convert(src)
        except Exception:
            if src.suffix.lower() != ".pdf" or args.engine != "auto":
                raise
            print(f"[提醒] MarkItDown 無法轉換 {src}；改用 pdf2txt。", file=sys.stderr)
            text = pdf2txt_engine.convert(src, output_format=args.format)
            engine = "pdf2txt"
        if not text and src.suffix.lower() == ".pdf" and args.engine == "auto":
            print(f"[提醒] MarkItDown 未擷取到 {src} 的文字；改用 pdf2txt。", file=sys.stderr)
            text = pdf2txt_engine.convert(src, output_format=args.format)
            engine = "pdf2txt"
    elif engine == "pdf2txt":
        if src.suffix.lower() != ".pdf":
            raise RuntimeError("pdf2txt 引擎僅支援 PDF。")
        text = pdf2txt_engine.convert(src, output_format=args.format)
    else:
        raise RuntimeError(f"未知引擎：{engine}")

    if not text.strip():
        raise RuntimeError(f"找不到可擷取文字：{src}。這可能是掃描或圖片型 PDF；請先使用 OCR 或查看原始頁面。")
    if missing_pages:
        pages = "、".join(map(str, missing_pages))
        warning = f"PDF 第 {pages} 頁沒有可擷取文字；請查看原始頁面或使用 OCR。"
        print(f"[提醒] {warning}", file=sys.stderr)
        text = f"轉檔提醒：{warning}\n\n{text}"
    write_text(dest, text)
    print(f"[完成] {engine}: {src} -> {dest}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="將文件轉成 Markdown 或文字檔。")
    parser.add_argument("input", help="輸入檔案或資料夾")
    parser.add_argument("-o", "--output", help="輸出檔案或資料夾", default=None)
    parser.add_argument("--engine", choices=["auto", "markitdown", "pdf2txt"], default="auto")
    parser.add_argument("--format", choices=["md", "txt"], default="md")
    parser.add_argument("--recursive", action="store_true", help="遞迴處理子資料夾")
    parser.add_argument("--vertical-text", action="store_true", help="直行中文教材 PDF 優先使用 pdf2txt")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    src = Path(args.input)
    output = Path(args.output) if args.output else None

    if not src.exists():
        parser.error(f"找不到輸入路徑：{src}")
    if src.is_file() and src.suffix.lower() in {".doc", ".ppt"}:
        parser.error(f"無法直接轉換舊版 {src.suffix.lower()}；請先改存成 .docx 或 .pptx：{src}")
    if src.is_file() and src.suffix.lower() in {".md", ".txt"}:
        parser.error(f"輸入已是文字檔，不需要轉換：{src}")

    input_is_dir = src.is_dir()
    files = iter_inputs(src, recursive=args.recursive)
    if not files:
        parser.error(f"找不到可轉換的檔案：{src}")

    try:
        for file_path in files:
            if input_is_dir and args.recursive and output:
                relative = file_path.relative_to(src).with_suffix(".txt" if args.format == "txt" else ".md")
                dest = output / relative
            else:
                dest = output_path_for(file_path, output, input_is_dir=input_is_dir, output_format=args.format)
            convert_one(file_path, dest, args)
    except Exception as exc:
        print(f"[錯誤] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
