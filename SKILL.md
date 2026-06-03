---
name: doc2md-toolkit
description: Convert teacher-provided documents into Markdown or UTF-8 text for AI workflows using the doc2md CLI. Use when Codex needs to extract or convert content from PDFs, Word documents, PowerPoint files, Excel files, HTML, CSV, JSON, XML, EPUB, folders of documents, Chinese teaching materials, vertical Chinese textbook PDFs, or teacher guide files before summarizing, lesson planning, creating worksheets, or building an AI teaching workbench artifact.
---

# doc2md-toolkit

Use this skill when a task needs source documents converted into Markdown or text before analysis, lesson planning, worksheet generation, summarization, or teaching material production.

## Core Workflow

1. Identify the source file or folder and desired output folder.
2. Install the toolkit if `doc2md` is unavailable.
3. For Chinese teaching-material PDFs, convert with `pdf2txt` by default and save Markdown as the primary source.
4. For Word, PowerPoint, Excel, HTML, CSV, JSON, XML, EPUB, and general non-teaching PDFs, use MarkItDown.
5. For scanned PDFs, image-only files, OCR-heavy documents, complex tables, formulas, or mixed layouts, do not pretend conversion is complete; mark the file as needing OCR or human confirmation.
6. Use UTF-8 output artifacts as the source of truth.
7. Continue the teaching or analysis task from the converted `.md` or `.txt` files.

## Install

From the toolkit repo root:

```powershell
pip install -e .
```

For broader Office/document support:

```powershell
pip install -e ".[all]"
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
- For scanned PDFs, image-only documents, OCR-heavy files, complex layout, tables, or formulas, do not pretend conversion is complete. Mark the file as needing OCR or human confirmation before using another specialized tool.

Examples:

```powershell
doc2md "一般文件.docx" --engine markitdown
doc2md "國語教材.pdf" --engine pdf2txt
doc2md "直行教材.pdf" --vertical-text
```

For teaching-material PDFs, the practical SOP is:

```text
pdf2txt Markdown = primary source
MarkItDown = not recommended for Chinese textbook/teacher-guide PDFs
OCR or human confirmation = needed for scanned/image-only files
```

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
