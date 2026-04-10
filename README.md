# DataClear

建筑规范 PDF 文档结构化处理工具链 — 将 PDF 转换为可入库的 DOCX 和 PPTX。

## 功能概览

```
PDF → MinerU 解析 → Markdown + images → 预处理 ─┬→ DOCX（可入库）
                                                  └→ PPTX（可演示）
```

| 能力 | 说明 |
|------|------|
| PDF 解析 | MinerU VLM 模型提取文字、表格、图片 |
| 表格修复 | HTML `<table>` → Markdown pipe table |
| DOCX 生成 | pandoc 转换，保留标题层级、表格、图片 |
| PPTX 生成 | 6 种风格模板，自动拆分长内容，多图布局 |
| 品牌逆向 | 从现有 PPT 提取配色/字体生成自定义风格 |

## 快速开始

### 安装依赖

```bash
pip install python-pptx          # PPTX 生成
# pandoc 安装（DOCX 生成需要）：
# macOS: brew install pandoc
# Windows: winget install --id JohnMacFarlane.Pandoc -e
# Linux: apt install pandoc
```

### 使用方式

**Markdown → PPTX**
```bash
python scripts/md_to_pptx.py input.md -o output.pptx --style=corporate
```

**Markdown → DOCX**
```bash
python scripts/md_to_docx_pandoc.py input.md -o output.docx
```

**批处理全部文档**
```bash
bash process_all.sh
```

## PPT 风格模板

6 种内置风格，通过 `--style` 参数选择：

| 风格 | 主色 | 适用场景 |
|------|------|---------|
| `corporate` (默认) | Navy #1E3A5F | 企业汇报 |
| `government` | 深蓝 #003366 + 红 #CC0000 | 政府标准文件 |
| `education` | 蓝 #2E5090 + 绿 #2FBF71 | 培训教材 |
| `minimal` | 灰 #555555 | 高管演示 |
| `technical` | 黑 #1A1A1A + 蓝 #0066CC | 工程技术 |
| `warm` | 棕 #B8764F + 橙 #E67E22 | 安全文化培训 |

### 品牌 PPT 逆向工程

从现有品牌 PPT 提取风格，生成自定义模板：

```bash
python .claude/skills/md-to-pptx/scripts/extract_style.py brand.pptx -o brand.json
python scripts/md_to_pptx.py input.md --style-file=brand.json
```

## PPT 图片支持

**简写引用** — 图片按编号命名（`01.png`, `02.png`），markdown 中简写：
```markdown
![图1]
```

**多图布局** — 连续图片自动合并到同一页：
```markdown
![图1]
![图2]
```
加 `---` 分隔则上下排列，不加则左右并排。

| 图片数 | 默认布局 | 加 `---` |
|--------|---------|---------|
| 1 | 居中最大化 | — |
| 2 | 左右并排 | 上下并列 |
| 3 | 上1下2 | 左1右2 |
| 4+ | 2xN 网格 | 2xN 网格 |

## Claude Code Skills

本项目包含两个独立的 Claude Code Skill，可通过斜杠命令调用：

| Skill | 命令 | 触发词 |
|-------|------|--------|
| md-to-pptx | `/md-to-pptx` | "做PPT"、"转PPT"、"make slides" |
| md-to-docx | `/md-to-docx` | "转docx"、"做文档"、"make word" |

### 安装 Skill

```bash
# 方法 1：手动复制到全局
cp -r .claude/skills/md-to-pptx ~/.claude/skills/
cp -r .claude/skills/md-to-docx ~/.claude/skills/

# 方法 2：项目内直接使用（已内置）
```

## 项目结构

```
dataclear/
├── .claude/skills/             # Claude Code Skills（独立产品）
│   ├── md-to-pptx/            #   Markdown→PPTX（6风格+逆向工程）
│   └── md-to-docx/            #   Markdown→DOCX（pandoc）
├── scripts/                    # CLI 入口（薄委托层）
│   ├── fix_mineru_md.py        #   HTML表格→Markdown表格预处理
│   ├── md_to_docx_pandoc.py    #   → md-to-docx skill
│   └── md_to_pptx.py           #   → md-to-pptx skill
├── process_all.sh              # 批处理脚本
└── data/documents/             # 文档数据（gitignore）
```

## 依赖

| 工具 | 安装 | 用途 |
|------|------|------|
| Python 3.8+ | 系统自带 | 脚本运行 |
| python-pptx | `pip install python-pptx` | PPTX 生成 |
| pandoc | 见上方安装说明 | DOCX 生成 |
| MinerU | `pip install -U "mineru[all]"` | PDF 解析（可选） |

## License

MIT
