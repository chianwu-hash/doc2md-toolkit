from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .detect import choose_engine, iter_inputs
from .engines import markitdown_engine, mineru_engine, pdf2txt_engine


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
    engine = choose_engine(src, args.engine, vertical_text=args.vertical_text, ocr=args.ocr)

    if engine == "markitdown":
        text = markitdown_engine.convert(src)
        if not text and src.suffix.lower() == ".pdf":
            text = pdf2txt_engine.convert(src, output_format=args.format)
        write_text(dest, text)
    elif engine == "pdf2txt":
        if src.suffix.lower() != ".pdf":
            raise RuntimeError("The pdf2txt engine only supports PDF input.")
        write_text(dest, pdf2txt_engine.convert(src, output_format=args.format))
    elif engine == "mineru":
        out_dir = dest if dest.suffix == "" else dest.parent
        mineru_engine.convert(src, out_dir, backend=args.mineru_backend)
    else:
        raise RuntimeError(f"Unknown engine: {engine}")

    print(f"[ok] {engine}: {src} -> {dest}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert documents to Markdown or text.")
    parser.add_argument("input", help="Input file or folder")
    parser.add_argument("-o", "--output", help="Output file or folder", default=None)
    parser.add_argument("--engine", choices=["auto", "markitdown", "pdf2txt", "mineru"], default="auto")
    parser.add_argument("--format", choices=["md", "txt"], default="md")
    parser.add_argument("--recursive", action="store_true", help="Process folders recursively")
    parser.add_argument("--vertical-text", action="store_true", help="Prefer pdf2txt for vertical Chinese textbook PDFs")
    parser.add_argument("--ocr", action="store_true", help="Prefer MinerU for scanned or OCR-heavy documents")
    parser.add_argument("--mineru-backend", default="pipeline", help="MinerU backend, default: pipeline")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    src = Path(args.input)
    output = Path(args.output) if args.output else None

    if not src.exists():
        parser.error(f"Input does not exist: {src}")

    input_is_dir = src.is_dir()
    files = iter_inputs(src, recursive=args.recursive)
    if not files:
        parser.error(f"No supported files found: {src}")

    try:
        for file_path in files:
            if input_is_dir and args.recursive and output:
                relative = file_path.relative_to(src).with_suffix(".txt" if args.format == "txt" else ".md")
                dest = output / relative
            else:
                dest = output_path_for(file_path, output, input_is_dir=input_is_dir, output_format=args.format)
            convert_one(file_path, dest, args)
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
