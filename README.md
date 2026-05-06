# doc2md-toolkit

一個整合教材友善 `pdf2txt`、一般文件用 MarkItDown、以及進階 MinerU 輔助流程的文件轉 Markdown / Text 工具包。

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
| 中文教材、備課用書、課本 PDF、直行文字 PDF、一字一行抽文字 | `pdf2txt` |
| Word、PowerPoint、Excel、HTML、CSV、JSON、XML、EPUB、一般非教材 PDF | `markitdown` |
| 複雜表格、多欄版面、圖片題、掃描/OCR、公式 | MinerU API 或進階 `mineru` |

教材 PDF 的預設 SOP：

1. 先用 `pdf2txt` 轉成 `.md`，作為正式文字來源。
2. 若表格、圖片題或多欄版面看不清楚，再用 MinerU API 輔助比對。
3. 不建議把 MarkItDown 當中文教材 PDF 的主流程；它較適合 Office 與一般文件。

## 安裝

輕量版：

```powershell
pip install -e .
```

完整 MarkItDown 依賴（主要給 Office / 一般文件使用）：

```powershell
pip install -e ".[all]"
```

本機 MinerU 依賴較重，只建議進階使用者在硬體足夠時安裝。一般情況優先使用 MinerU API：

```powershell
pip install -e ".[mineru]"
```

若使用 MinerU API，請把 token 放在環境變數，不要提交到 Git：

```powershell
$env:MINERU_API_TOKEN="你的 token"
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

對中文教材、備課用書、課本 PDF，MarkItDown 不建議作為主流程；實測常不如 `pdf2txt` 穩定，表格也未必優於 MinerU。

### pdf2txt

內建的 PDF 文字抽取器，使用 PyMuPDF。特別針對中文直行教材常見的「抽出後一個字一行」問題，會嘗試把直行文字串接成較容易閱讀的內容。

這是中文教材 PDF 的主力流程。建議先輸出 `.md`，再用轉出的 Markdown 作為出題、摘要、備課與 AI 分析的主要依據。

### MinerU

適合複雜文件解析、掃描件、表格、公式、多欄版面與 OCR。

建議定位為輔助流程：

- 平常先用 `pdf2txt`。
- 遇到複雜表格、圖片題、Q&A 表格或版面混雜，再請 MinerU 出場。
- 優先使用 MinerU API，避免在一般教學電腦上安裝大型本機依賴。
- 本機 `mineru` CLI 屬進階用法；若硬體不足，請改用 API 或回到 `pdf2txt`。

## 授權與第三方工具

本專案本身採 MIT License。

- MarkItDown 是 Microsoft 的開源工具，請遵守其授權。
- MinerU 採 MinerU Open Source License，基於 Apache 2.0 並包含額外條件，使用前請確認授權需求。
- 本專案預設不內嵌 MarkItDown 或 MinerU 原始碼，只透過套件或 CLI 呼叫。
