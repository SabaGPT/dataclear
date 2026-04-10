---
name: md-to-docx
description: >
  Convert Markdown files to Word documents (DOCX) using pandoc.
  Trigger when: user says "convert to docx", "make word", "markdown to word",
  "转docx", "做文档", "生成Word", or references creating Word documents
  from markdown content.
  Supports pipe tables, images, and custom Word style templates.
---

# Markdown → DOCX Converter

Convert Markdown files into structured Word documents using pandoc.
Handles headings, pipe tables, images, and optional custom Word style templates.

**Engine**: pandoc (system binary) with `pipe_tables+grid_tables+multiline_tables`

## Prerequisites

**Required**: pandoc
```bash
# macOS
brew install pandoc

# Windows
winget install --id JohnMacFarlane.Pandoc -e

# Linux
apt install pandoc
```

## Workflow

### Step 1: Ensure pandoc is installed

```bash
pandoc --version
```

### Step 2: Identify Input and Output

**Scenario A — File path:**
```
Input:  document.md
Output: document.docx (default)
```

**Scenario B — Dataclear document directory:**
```
Input:  <dir>/output/fixed.md
Output: <dir>/output/clean.docx
Images: --resource-path=<dir>/mineru_output
```

**Scenario C — Input has HTML tables:**
Preprocess first:
```bash
python scripts/fix_mineru_md.py raw.md -o fixed.md
```

### Step 3: Run Conversion

```bash
python ${CLAUDE_SKILL_DIR}/scripts/md_to_docx_pandoc.py <input.md> \
  -o <output.docx> \
  --resource-path=<images_dir>
```

**Arguments:**

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `input_md` | Yes | — | Input Markdown file |
| `-o, --output` | No | `<input>.docx` | Output DOCX path |
| `--reference-doc` | No | — | Custom Word template (.docx) |
| `--resource-path` | No | `.` | Image resolution directory |

### Step 4: Report Results

On success: `[OK] 转换完成: output.docx`

### Step 5: Handle Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `未找到 pandoc` | pandoc not installed | Install pandoc |
| `输入文件不存在` | Wrong path | Check file path |
| Images missing | Wrong resource-path | Set `--resource-path` to images directory |

## Supported Markdown Elements

| Element | DOCX Result |
|---------|-------------|
| `# H1` ~ `###### H6` | Heading 1-6 styles |
| Paragraphs | Normal text |
| Pipe tables | Native Word tables |
| Grid/multiline tables | Native Word tables |
| `![](path)` | Embedded images |
| `**bold**` / `*italic*` | Bold / Italic |
| Lists | Numbered/bulleted lists |

## Examples

```bash
# Basic conversion
python ${CLAUDE_SKILL_DIR}/scripts/md_to_docx_pandoc.py report.md -o report.docx

# With images
python ${CLAUDE_SKILL_DIR}/scripts/md_to_docx_pandoc.py doc.md \
  -o doc.docx --resource-path=./images

# With custom Word template
python ${CLAUDE_SKILL_DIR}/scripts/md_to_docx_pandoc.py doc.md \
  -o doc.docx --reference-doc=template.docx
```
