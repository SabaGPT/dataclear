# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

建筑规范PDF → ima可入库的结构化docx（图文完整、表格可检索、零OCR错字）。

处理多份中国建筑消防安全标准文档（GB 55037-2022 实施指南 Parts 1-01~1-05 及相关标准）。

## Pipeline

```
PDF → MinerU解析 → Markdown + images/ → fix_mineru_md.py预处理 ─┬→ pandoc → clean.docx → ima入库
                                                                 └→ md_to_pptx.py → clean.pptx
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

### Step 3 (并列): md转pptx
```bash
python ../../../scripts/md_to_pptx.py output/fixed.md -o output/clean.pptx --resource-path=mineru_output
```
使用 `python-pptx` 将 Markdown 转换为结构化 PowerPoint（16:9 宽屏）。设计风格参考 baoyu-slide-deck（corporate 风格）。自动拆分长内容、大表格，图片居中最大化显示。与 Step 3 的 docx 转换并列，独立使用。

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
├── .claude/skills/             # Claude Code Skills
│   ├── md-to-pptx/            #   Markdown→PPTX skill（独立产品）
│   │   ├── SKILL.md            #     Skill 定义和工作流
│   │   ├── scripts/md_to_pptx.py #  转换引擎（6种风格模板）
│   │   ├── scripts/extract_style.py # 品牌PPT逆向工程
│   │   └── references/         #     设计规范和内容规则
│   └── md-to-docx/            #   Markdown→DOCX skill（独立产品）
│       ├── SKILL.md            #     Skill 定义和工作流
│       └── scripts/md_to_docx_pandoc.py # 转换引擎（pandoc）
├── scripts/                    # 应用代码（薄委托层）
│   ├── fix_mineru_md.py        #   HTML表格→Markdown表格预处理
│   ├── md_to_docx_pandoc.py    #   → skill 入口（委托给 .claude/skills/）
│   └── md_to_pptx.py           #   → skill 入口（委托给 .claude/skills/）
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
│               ├── clean.docx  #     最终docx
│               └── clean.pptx  #     最终pptx（可选）
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
| python-pptx | `pip install python-pptx` | Markdown→pptx |
| Python 3.8+ | System (`python` on Windows, not `python3`) | Scripts (fix_mineru_md.py 仅用 stdlib) |

## MinerU Config

Global config: `config/config.json` (language: zh-CN, model: VLM). Task DB: `data/mineru.db`.
