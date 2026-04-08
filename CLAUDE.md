# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

建筑规范PDF → ima可入库的结构化docx（图文完整、表格可检索、零OCR错字）。

处理多份中国建筑消防安全标准文档（GB 55037-2022 实施指南 Parts 1-01~1-05 及相关标准）。

## Pipeline (3 Steps)

```
PDF → MinerU解析 → Markdown + images/ → fix_mineru_md.py预处理 → pandoc → clean.docx → ima入库
```

### Step 1: MinerU解析 (already done)
MinerU v0.13.1 (VLM model + doclayout_yolo) extracted PDF into markdown, images, and JSON metadata.

### Step 2: 预处理
```bash
cd data/documents/<文档名>
python ../../../scripts/fix_mineru_md.py mineru_output/full.md -o output/fixed.md
```
Converts HTML `<table>` tags (which pandoc's markdown reader ignores) into Markdown pipe tables. Handles `rowspan`/`colspan`. Script uses only stdlib (`re`, `pathlib`).

### Step 3: pandoc转docx
```bash
python ../../../scripts/md_to_docx_pandoc.py output/fixed.md -o output/clean.docx --resource-path=mineru_output
```
Requires `pandoc`. Normalizes ATX headings then calls pandoc with `pipe_tables+grid_tables+multiline_tables`.

注意：需在文档数据目录下运行，pandoc 的 `--resource-path` 指向 `mineru_output` 以找到 `images/` 子目录。

### 一键批处理
```bash
bash process_all.sh            # 处理所有文档
bash process_all.sh "GB+35181-2025"  # 只处理指定文档
```
自动查找每个文档的 MinerU 源 markdown（优先级：MinerU_markdown_*.md > full.md > 任意.md），依次运行 fix_mineru_md.py 和 md_to_docx_pandoc.py。无源 markdown 的文档自动跳过。

**Windows注意**：`python3` 可能是 Windows Store stub（exit code 49）。`process_all.sh` 会自动检测并回退到 `python`。手动运行脚本时也应使用 `python` 而非 `python3`。

## Directory Structure

```
dataclear/
├── CLAUDE.md                   # 项目指引
├── .gitignore                  # 排除数据文件和敏感配置
├── scripts/                    # 应用代码（唯一副本）
│   ├── fix_mineru_md.py        #   HTML表格→Markdown表格预处理
│   └── md_to_docx_pandoc.py    #   Markdown→docx转换
├── docs/                       # 项目文档
│   └── technical-spec.md       #   技术规格文档
├── config/                     # MinerU配置（gitignore排除）
│   └── config.json             #   含API token，勿提交
├── data/                       # 所有文档处理数据（gitignore排除）
│   ├── mineru.db               #   MinerU任务数据库
│   └── documents/              #   各文档目录
│       └── <文档名>/
│           ├── source/         #   源PDF
│           ├── mineru_output/  #   MinerU原始输出（勿编辑）
│           │   ├── images/     #     提取的图片(SHA-256哈希文件名)
│           │   ├── *.json      #     结构化内容、块级数据、布局等
│           │   └── *.md        #     原始Markdown备份
│           └── output/         #   处理产物
│               ├── fixed.md    #     预处理后的中间稿
│               └── clean.docx  #     最终docx
```

### 文档目录列表

| 目录名 | 说明 |
|--------|------|
| `DB32` | 江苏省地方标准 DB32/T 5183-2025 |
| `建筑防火通用规范 GB 55037-2022实施指南(1-01）` | GB 55037-2022 Part 1-01 |
| `建筑防火通用规范 GB 55037-2022实施指南(1-02)` | GB 55037-2022 Part 1-02 |
| `建筑防火通用规范 GB 55037-2022实施指南(1-03)` | GB 55037-2022 Part 1-03 |
| `建筑防火通用规范 GB 55037-2022实施指南(1-04)` | GB 55037-2022 Part 1-04 |
| `建筑防火通用规范 GB 55037-2022实施指南(1-05)` | GB 55037-2022 Part 1-05 |
| `GB+35181-2025` | 国家标准 GB 35181-2025 |
| `《教育系统重大事故隐患判定指南》` | 教育系统安全指南 |
| `浙江省消防技术规范难点问题操作技术指南（2025版）` | 浙江省地方指南 |

## Known Issues

- **Heading levels**: MinerU outputs all visually prominent lines as `#` (H1), including chapter titles, section titles, and annotation markers like【条文要点】. This may cause over-fragmented chunks in ima. A lua filter (~20 lines) can fix this if ima testing shows problems.
- **OCR quality**: MinerU's VLM engine has near-zero OCR errors on these documents (validated on 1-03, 73 pages). However some artifacts exist in raw output (e.g., "通川" for "通用"). Check the MinerU markdown vs the edited markdown.

## Dependencies

| Tool | Install | Purpose |
|------|---------|---------|
| MinerU | `pip install -U "mineru[all]"` | PDF解析 (already done) |
| pandoc | `winget install --id JohnMacFarlane.Pandoc -e` | Markdown→docx |
| Python 3.8+ | System (`python` on Windows, not `python3`) | Scripts use only stdlib |

## MinerU Config

Global config: `config/config.json` (language: zh-CN, model: VLM). Task DB: `data/mineru.db`.
