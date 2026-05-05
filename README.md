# doc2md-toolkit

一個整合 MarkItDown、教材友善 `pdf2txt`、以及 optional MinerU 的文件轉 Markdown / Text 工具包。

目標是讓使用者只記一個指令：

```powershell
doc2md "檔案.pdf"
```

## Codex skill

這個 repo 也可以作為 Codex skill 使用。當老師或使用者需要把 PDF、Word、PowerPoint、教師手冊或教材檔轉成 AI 容易處理的 Markdown / Text 時，可以請 Codex 安裝並使用這個 GitHub 專案。

給 Codex 的建議說法：

```text
請從這個 GitHub 專案安裝並使用 doc2md-toolkit，協助我把教材文件轉成 Markdown 或 UTF-8 文字，再用轉換後的內容建立教學成果：

https://github.com/chianwu-hash/doc2md-toolkit
```

## 工具分工

| 情境 | 建議引擎 |
| --- | --- |
| 一般 PDF、Word、PPT、Excel、HTML、CSV、JSON | `markitdown` |
| 國語教材、中文教材、直行文字 PDF、一字一行抽文字 | `pdf2txt` |
| 掃描 PDF、複雜版面、表格、公式、OCR | `mineru` |

## 安裝

輕量版：

```powershell
pip install -e .
```

完整 MarkItDown 依賴：

```powershell
pip install -e ".[all]"
```

MinerU 很重，建議需要時再裝：

```powershell
pip install -e ".[mineru]"
```

## 使用

自動判斷：

```powershell
doc2md "example.pdf"
```

指定輸出：

```powershell
doc2md "example.docx" -o "example.md"
```

資料夾批次轉換：

```powershell
doc2md "D:\in\documents" -o "D:\out\md"
```

遞迴處理資料夾：

```powershell
doc2md "D:\in\documents" -o "D:\out\md" --recursive
```

指定引擎：

```powershell
doc2md "一般文件.docx" --engine markitdown
doc2md "國語教材.pdf" --engine pdf2txt
doc2md "掃描文件.pdf" --engine mineru
```

輸出純文字：

```powershell
doc2md "國語教材.pdf" --engine pdf2txt --format txt
```

## 引擎說明

### MarkItDown

適合一般文件轉 Markdown。支援 PDF、Office 文件、HTML、CSV、JSON、XML、EPUB 等常見格式。

### pdf2txt

內建的 PDF 文字抽取器，使用 PyMuPDF。特別針對中文直行教材常見的「抽出後一個字一行」問題，會嘗試把直行文字串接成較容易閱讀的內容。

### MinerU

適合複雜文件解析、掃描件、表格、公式、多欄版面與 OCR。此工具不預設安裝，避免讓一般使用者背負大型模型與依賴。

## 授權與第三方工具

本專案本身採 MIT License。

- MarkItDown 是 Microsoft 的開源工具，請遵守其授權。
- MinerU 採 MinerU Open Source License，基於 Apache 2.0 並包含額外條件，使用前請確認授權需求。
- 本專案預設不內嵌 MarkItDown 或 MinerU 原始碼，只透過套件或 CLI 呼叫。
