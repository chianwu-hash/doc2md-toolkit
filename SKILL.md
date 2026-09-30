---
name: doc2md
description: Convert teacher-provided documents into Markdown or UTF-8 text for AI workflows using the doc2md CLI. Use when Codex needs to extract or convert content from PDFs, Word documents, PowerPoint files, Excel files, HTML, CSV, JSON, XML, EPUB, folders of documents, Chinese teaching materials, vertical Chinese textbook PDFs, or teacher guide files before summarizing, lesson planning, creating worksheets, or building an AI teaching workbench artifact.
---

# doc2md-toolkit

Use this skill when a task needs source documents converted into Markdown or text before analysis, lesson planning, worksheet generation, summarization, or teaching material production.

## Core Workflow

1. Identify the source file or folder and desired output folder.
2. Check whether the document contains student, parent, confidential, or unpublished information before using any external service. The default CLI stays local.
3. Install the toolkit if `doc2md` is unavailable.
4. Triage PDFs by page count and layout before deep conversion:
   - For 1-3 page schedules, notices, simple tables, or visually clear forms, run quick text/table extraction first, then render page images and visually verify when text is mojibake, columns break, red/marked changes matter, or the user's goal is comparison rather than full transcription.
   - Treat extracted text as a draft and the rendered page image as the authority when the PDF text layer is corrupt or layout-critical.
   - For longer, text-heavy, or reusable documents, prefer normal extraction first; render images only to spot-check unclear pages.
5. For Chinese teaching-material PDFs with recognizable filenames, `auto` chooses `pdf2txt`. Otherwise use `--engine pdf2txt` explicitly and save Markdown as the primary source.
6. For `.docx`, `.pptx`, `.xlsx`, `.xls`, HTML, CSV, JSON, XML, EPUB, and general non-teaching PDFs, use MarkItDown. Convert legacy `.doc` or `.ppt` to a newer Office format first.
7. For scanned PDFs, image-only files, or PDFs without a text layer up to 10 pages, the CLI reports no extractable text. If only some pages lack text, the output marks them for review. Convert pages to images and use small-batch OCR or AI vision as a separate rescue path only after checking data-sharing permission.
8. For scanned/image-only documents over 10 pages, complex tables, formulas, or mixed layouts, do not pretend conversion is complete; mark the file as needing formal OCR or human confirmation.
9. Use UTF-8 output artifacts as the source of truth.
10. Continue the teaching or analysis task from the converted `.md` or `.txt` files.

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

- Use `--engine pdf2txt` or `--vertical-text` when a Chinese teaching PDF has an ambiguous filename or extracts as one character per line. `auto` only recognizes common teaching terms in the filename.
- Use `markitdown` for Word, PowerPoint, Excel, HTML, CSV, JSON, XML, EPUB, and general non-teaching PDFs.
- For short PDF schedules, notices, forms, and simple tables, choose the fastest reliable path: quick extraction for draft text plus rendered-page visual verification when layout, colors, or text-layer corruption could change the answer.
- For scanned PDFs, image-only documents, or PDFs without a text layer up to 10 pages, convert pages to images and use small-batch OCR or AI vision as a rescue path.
- For scanned/image-only documents over 10 pages, complex layout, tables, or formulas, do not pretend conversion is complete. Mark the file as needing formal OCR or human confirmation before using another specialized tool.

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
small-batch image OCR or AI vision = acceptable rescue path for scanned/image-only files up to 10 pages
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
