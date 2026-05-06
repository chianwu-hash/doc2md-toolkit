---
name: doc2md-toolkit
description: Convert teacher-provided documents into Markdown or UTF-8 text for AI workflows using the doc2md CLI. Use when Codex needs to extract or convert content from PDFs, Word documents, PowerPoint files, Excel files, HTML, CSV, JSON, XML, EPUB, folders of documents, Chinese teaching materials, vertical Chinese textbook PDFs, scanned/OCR-heavy PDFs, or teacher guide files before summarizing, lesson planning, creating worksheets, or building an AI teaching workbench artifact.
---

# doc2md-toolkit

Use this skill when a task needs source documents converted into Markdown or text before analysis, lesson planning, worksheet generation, summarization, or teaching material production.

## Core Workflow

1. Identify the source file or folder and desired output folder.
2. Install the toolkit if `doc2md` is unavailable.
3. For Chinese teaching-material PDFs, convert with `pdf2txt` by default and save Markdown as the primary source.
4. Use MinerU only as a secondary check when complex tables, image questions, OCR, or mixed layouts make `pdf2txt` unclear.
5. Use UTF-8 output artifacts as the source of truth.
6. Continue the teaching or analysis task from the converted `.md` or `.txt` files.

## Install

From the toolkit repo root:

```powershell
pip install -e .
```

For broader Office/document support:

```powershell
pip install -e ".[all]"
```

Local MinerU dependencies can be heavy. Prefer MinerU API when OCR, scanned PDFs, formulas, tables, or complex layouts require a second pass. Install local MinerU only when the machine has enough resources and the user explicitly wants local processing:

```powershell
pip install -e ".[mineru]"
```

If the user provided the GitHub URL rather than a local checkout, clone or download the repo first, then install from its root.

## Convert

Convert one document beside the source:

```powershell
doc2md "教材.pdf"
```

Specify an output file:

```powershell
doc2md "教材.docx" -o "output\教材.md"
```

Convert a folder:

```powershell
doc2md "data\source-docs" -o "data\converted-md"
```

Convert a folder recursively:

```powershell
doc2md "data\source-docs" -o "data\converted-md" --recursive
```

Output plain text:

```powershell
doc2md "教材.pdf" --format txt
```

## Engine Selection

Prefer `--engine auto` unless there is a clear reason to choose one.

- Use `pdf2txt` or `--vertical-text` as the main path for Chinese teaching materials, Mandarin textbooks, teacher guides, textbook PDFs, and vertical Chinese PDFs that extract as one character per line.
- Use `markitdown` for Word, PowerPoint, Excel, HTML, CSV, JSON, XML, EPUB, and general non-teaching PDFs.
- Use MinerU API as a second-pass reference for scanned PDFs, OCR-heavy documents, image questions, complex layout, tables, or formulas.
- Use local `mineru` / `--ocr` only for advanced local setups. Do not make it the default on ordinary teaching machines.

Examples:

```powershell
doc2md "一般文件.docx" --engine markitdown
doc2md "國語教材.pdf" --engine pdf2txt
doc2md "直行教材.pdf" --vertical-text
doc2md "掃描文件.pdf" --engine mineru
```

For teaching-material PDFs, the practical SOP is:

```text
pdf2txt Markdown = primary source
MinerU API output = helper for difficult tables/layouts
MarkItDown = not recommended for Chinese textbook/teacher-guide PDFs
```

If a MinerU API token is available, read it from `MINERU_API_TOKEN`; never paste tokens into tracked files or logs.

## Windows And Chinese Text

When running on Windows with Chinese/CJK content:

- Treat terminal-rendered Chinese as untrusted.
- Do not copy mojibake from terminal output into files.
- Read the generated UTF-8 `.md` or `.txt` files in VS Code or another UTF-8-aware tool.
- If `windows-powershell-encoding-skill` is available, use it together with this skill.

## AI Teaching Workbench Pattern

For teacher workshops, convert teacher materials into a workbench folder such as:

```text
AI教學工作台-我的成果/
├─ source-docs/
├─ converted-md/
└─ teaching-package/
```

Then use the converted files to create:

```text
teaching-package/
├─ 01-課程流程.md
├─ 02-課堂提問與活動.md
├─ 03-學生任務單.md
└─ 04-課後調整筆記.md
```

Keep conversion separate from generated teaching artifacts so the teacher can inspect the source text and revise outputs later.
