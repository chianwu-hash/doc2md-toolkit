# doc2md-toolkit

一個整合教材友善 `pdf2txt` 與一般文件用 MarkItDown 的文件轉 Markdown / Text 工具包。

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
| 10 頁以內的掃描 PDF、圖片型文件、沒有文字層的 PDF | 可先轉成逐頁圖片，再用小量 OCR 或 AI 視覺讀取救援 |
| 超過 10 頁的掃描 PDF、圖片型文件、複雜表格、公式、多欄版面 | 不在本工具主流程內，請先標記為需要正式 OCR 或人工確認 |

教材 PDF 的預設 SOP：

1. 先用 `pdf2txt` 轉成 `.md`，作為正式文字來源。
2. 檢查標題、段落、表格、頁碼、頁首頁尾與是否漏頁。
3. 若是 10 頁以內的掃描檔、圖片型文件或沒有文字層，可轉成逐頁圖片後，用小量 OCR 或 AI 視覺讀取救援。
4. 若超過 10 頁，或版面包含複雜表格、公式、多欄內容，請標記為需要正式 OCR 或人工確認。
5. 不建議把 MarkItDown 當中文教材 PDF 的主流程；它較適合 Office 與一般文件。

## 安裝

輕量版：

```powershell
pip install -e .
```

完整 MarkItDown 依賴（主要給 Office / 一般文件使用）：

```powershell
pip install -e ".[all]"
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
```

輸出純文字：

```powershell
doc2md "國語教材.pdf" --engine pdf2txt --format txt
```

## 引擎說明

### MarkItDown

適合一般文件轉 Markdown。支援 PDF、Office 文件、HTML、CSV、JSON、XML、EPUB 等常見格式。

對中文教材、備課用書、課本 PDF，MarkItDown 不建議作為主流程；實測常不如 `pdf2txt` 穩定。

### pdf2txt

內建的 PDF 文字抽取器，使用 PyMuPDF。特別針對中文直行教材常見的「抽出後一個字一行」問題，會嘗試把直行文字串接成較容易閱讀的內容。

這是中文教材 PDF 的主力流程。建議先輸出 `.md`，再用轉出的 Markdown 作為出題、摘要、備課與 AI 分析的主要依據。

### 掃描檔與 OCR

本工具不內建重型 OCR 流程。遇到 10 頁以內的掃描 PDF、圖片型文件或沒有文字層的 PDF，可以先轉成逐頁圖片，再用小量 OCR 或 AI 視覺讀取救援。若超過 10 頁，或版面包含複雜表格、公式、多欄內容，不要假裝已完整轉換；請先標記為需要正式 OCR 或人工確認，再視需求使用其他專門工具處理。

## 授權與第三方工具

本專案本身採 MIT License。

- MarkItDown 是 Microsoft 的開源工具，請遵守其授權。
- 本專案預設不內嵌 MarkItDown 原始碼，只透過套件呼叫。
