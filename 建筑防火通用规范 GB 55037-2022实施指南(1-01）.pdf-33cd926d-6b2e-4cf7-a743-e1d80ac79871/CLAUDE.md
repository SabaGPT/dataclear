# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

建筑规范PDF → ima可入库的结构化docx（图文完整、表格可检索、零OCR错字）。

This directory processes "《建筑防火通用规范》GB 55037-2022 实施指南 (Part 1-01)" — a Chinese national building fire safety standard. It is one of several documents under `D:/Akira/project/MinerU/` (Parts 1-01 through 1-05 plus related standards).

## Pipeline (3 Steps)

```
PDF → MinerU解析 → Markdown + images/ → fix_mineru_md.py预处理 → pandoc → clean.docx → ima入库
```

### Step 1: MinerU解析 (already done)
MinerU v0.13.1 (VLM model + doclayout_yolo) extracted PDF into markdown, images, and JSON metadata.

### Step 2: 预处理
```bash
python scripts/fix_mineru_md.py "建筑防火通用规范 GB 55037-2022实施指南(1-01）.md" -o fixed.md
```
Converts HTML `<table>` tags (which pandoc's markdown reader ignores) into Markdown pipe tables. Handles `rowspan`/`colspan`. Script uses only stdlib (`re`, `pathlib`).

### Step 3: pandoc转docx
```bash
python scripts/md_to_docx_pandoc.py fixed.md -o output/clean.docx
```
Requires `pandoc` (`winget install --id JohnMacFarlane.Pandoc -e`). Normalizes ATX headings then calls pandoc with `pipe_tables+grid_tables+multiline_tables`.

### Batch processing
```bash
python scripts/fix_mineru_md.py ./dir/ --batch -o ./fixed/
```

## Directory Structure

```
├── scripts/                # 流水线程式
│   ├── fix_mineru_md.py    #   HTML表格→Markdown表格预处理
│   └── md_to_docx_pandoc.py #  Markdown→docx转换
├── source/                 # 源PDF
│   └── 8d965c25-..._origin.pdf
├── mineru_output/          # MinerU原始输出（勿编辑）
│   ├── images/             #   提取的图片(SHA-256哈希文件名)
│   ├── MinerU_markdown_*.md #  原始Markdown备份
│   ├── content_list_v2.json #  结构化内容JSON
│   ├── block_list.json     #   块级提取数据
│   └── layout.json, *_model.json, *_content_list.json
├── output/                 # 最终产物
│   └── clean.docx
├── 建筑防火...md           # 可编辑主稿（图片路径: mineru_output/images/）
├── fixed.md                # 预处理后的中间稿
├── CLAUDE.md               # 项目指引
└── final-technical-spec.md # 技术规格文档
```

## Known Issues

- **Heading levels**: MinerU outputs all visually prominent lines as `#` (H1), including chapter titles, section titles, and annotation markers like【条文要点】. This may cause over-fragmented chunks in ima. A lua filter (~20 lines) can fix this if ima testing shows problems.
- **OCR quality**: MinerU's VLM engine has near-zero OCR errors on these documents (validated on 1-03, 73 pages). However some artifacts exist in raw output (e.g., "通川" for "通用"). Check the MinerU markdown vs the edited markdown.

## Dependencies

| Tool | Install | Purpose |
|------|---------|---------|
| MinerU | `pip install -U "mineru[all]"` | PDF解析 (already done) |
| pandoc | `winget install --id JohnMacFarlane.Pandoc -e` | Markdown→docx |
| Python 3.8+ | System | Scripts use only stdlib |

## MinerU Config

Global config: `D:/Akira/project/MinerU/config.json` (language: zh-CN, model: VLM). Task DB: `D:/Akira/project/MinerU/data/mineru.db`.
