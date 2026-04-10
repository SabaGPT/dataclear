---
name: md-to-pptx
description: >
  Convert Markdown files to structured PowerPoint presentations (PPTX).
  Trigger when: user says "make PPT", "create slides", "convert to pptx",
  "markdown to PowerPoint", "生成PPT", "做PPT", "转PPT", or references
  creating presentations from markdown content.
  Supports Chinese content, pipe tables, images, and automatic content splitting.
  Design style: baoyu-slide-deck corporate (16:9, navy title bars, clean layout).
---

# Markdown → PPTX Converter

Convert any Markdown document into a professional, structured PowerPoint file.
Self-contained skill with bundled Python script, design references, and content rules.

**Design**: baoyu-slide-deck corporate style — 16:9 widescreen, navy (#1E3A5F)
title bars, clean whitespace, professional Chinese typography.

**Engine**: `python-pptx` generating native text/table/image slides (searchable,
editable content — not image-based slides).

## Directory Structure

```
.claude/skills/md-to-pptx/
├── SKILL.md                          # This file — workflow definition
├── scripts/
│   └── md_to_pptx.py                # Conversion engine (Python, ~620 lines)
└── references/
    ├── design-style.md               # Color palette, typography, layout specs
    └── content-rules.md              # Heading→slide mapping, splitting rules
```

## Prerequisites

**Required**: Python 3.8+ and `python-pptx`:
```bash
pip install python-pptx
```

**Optional** (for image embedding): `Pillow` is auto-installed with python-pptx.

## Workflow

Follow these steps in order. This is a deterministic conversion — no user
confirmation rounds needed (unlike baoyu-slide-deck's interactive image generation).

### Step 1: Ensure Dependencies

Check that `python-pptx` is installed:
```bash
python -c "import pptx; print(f'python-pptx {pptx.__version__} OK')"
```
If missing, install it:
```bash
pip install python-pptx
```

### Step 2: Identify Input and Output

Determine the input Markdown file and output PPTX path.

**Scenario A — User gives a file path:**
```
Input:  /path/to/document.md
Output: /path/to/document.pptx  (default, same dir)
```

**Scenario B — User gives a dataclear document directory:**
```
Input:  <dir>/output/fixed.md
Output: <dir>/output/clean.pptx
Images: --resource-path=<dir>/mineru_output
```

**Scenario C — User pastes Markdown content:**
Save to a temporary file, then convert:
```bash
cat > /tmp/input.md << 'MDEOF'
<pasted content>
MDEOF
```

**Scenario D — Input has HTML tables (raw MinerU output):**
Preprocess first with `fix_mineru_md.py` if available:
```bash
python scripts/fix_mineru_md.py raw.md -o fixed.md
python ${CLAUDE_SKILL_DIR}/scripts/md_to_pptx.py fixed.md -o output.pptx
```

### Step 3: Run Conversion

Execute the bundled conversion script:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/md_to_pptx.py <input.md> \
  -o <output.pptx> \
  --resource-path=<images_directory>
```

**All arguments:**

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `input_md` | Yes | — | Input Markdown file path |
| `-o, --output` | No | `<input>.pptx` | Output PPTX file path |
| `--resource-path` | No | `.` | Directory to resolve `![](images/...)` paths |

### Step 4: Report Results

On success, report:
- Output file path and size
- Number of slides generated
- Breakdown by type (cover, section, content, table, image)

**Success output example:**
```
[OK] 转换完成: output/clean.pptx (18 张幻灯片)
```

### Step 5: Handle Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: pptx` | python-pptx not installed | `pip install python-pptx` |
| `输入文件不存在` | Wrong file path | Check path, use absolute path |
| `[图片未找到: ...]` | Image not in resource-path | Check `--resource-path` points to images dir |

## Supported Markdown Elements

| Element | Example | PPTX Result |
|---------|---------|-------------|
| H1 heading (first) | `# Document Title` | **Cover slide**: navy background, centered title |
| H1 heading (others) | `# Chapter 3` | **Section divider**: navy band, centered title |
| H2/H3+ heading | `## 3.1 Details` | **Content slide**: navy title bar + body area |
| Paragraph | Plain text | Body text, auto-split across slides if long |
| Pipe table | `\| col \| col \|` | **Table slide**: native PPTX table with styled header |
| Image | `![alt](path.png)` | **Image slide**: centered, maximized, aspect-preserved |
| List | `- item` / `1. item` | Body text lines |
| Bold | `**text**` | Plain text (markdown formatting stripped) |

## Design Specification

Full details in `references/design-style.md`. Summary:

### Colors
- **Navy** (#1E3A5F): Title bars, cover, section dividers, table headers
- **Accent Blue** (#2B6CB0): Accent lines, highlights
- **White** (#FFFFFF): Backgrounds, text on dark
- **Dark Gray** (#2D2D2D): Body text

### Typography
- **Titles**: Microsoft YaHei Bold, 24-36pt
- **Body**: Microsoft YaHei, 16pt
- **Tables**: Microsoft YaHei, 12-13pt

### Slide Layouts (5 types)
1. **Cover** — full navy background, large centered title, accent line
2. **Section** — white with navy horizontal band, centered section title
3. **Content** — navy title bar top, body text below
4. **Table** — navy title bar top, native styled table below
5. **Image** — navy title bar top, centered maximized image below

### Rules
- 16:9 widescreen (13.333 × 7.5 inches)
- No footers, no page numbers, no logos
- Minimum 10% margin from all edges
- One main idea per slide

## Content Splitting Rules

Full details in `references/content-rules.md`. Summary:

| Parameter | Threshold | Action when exceeded |
|-----------|-----------|---------------------|
| Body text lines | 12 | Split to next slide with "(续N)" title suffix |
| Body text chars | 400 | Split to next slide |
| Table rows | 10 | Split table, repeat header row |

Split points: paragraph boundary > sentence boundary > character boundary.

## Examples

### Single file conversion
```bash
python ${CLAUDE_SKILL_DIR}/scripts/md_to_pptx.py report.md -o report.pptx
```

### With image directory
```bash
python ${CLAUDE_SKILL_DIR}/scripts/md_to_pptx.py doc.md \
  -o slides.pptx \
  --resource-path=./images
```

### Dataclear pipeline integration
```bash
# From document directory
cd data/documents/GB+35181-2025
python ../../../.claude/skills/md-to-pptx/scripts/md_to_pptx.py \
  output/fixed.md -o output/clean.pptx --resource-path=mineru_output
```

### Batch conversion (all documents)
```bash
for doc_dir in data/documents/*/; do
  fixed="$doc_dir/output/fixed.md"
  [ -f "$fixed" ] || continue
  python .claude/skills/md-to-pptx/scripts/md_to_pptx.py "$fixed" \
    -o "$doc_dir/output/clean.pptx" \
    --resource-path="$doc_dir/mineru_output"
  echo "[OK] $(basename $doc_dir)"
done
```

## Architecture

```
Input: Markdown text
         │
         ▼
┌─────────────────┐
│ normalize_headings│ — Fix "##标题" → "## 标题"
└────────┬────────┘
         ▼
┌─────────────────┐
│ parse_markdown   │ — State machine: headings, tables, images, lists, paragraphs
│                  │   → list[Section(level, title, blocks)]
└────────┬────────┘
         ▼
┌─────────────────┐
│ plan_slides      │ — Map sections to slide types, split long content
│                  │   → list[SlideData(layout, title, body/table/image)]
└────────┬────────┘
         ▼
┌─────────────────┐
│ create_pptx      │ — python-pptx: generate slides per layout type
│                  │   → .pptx file
└─────────────────┘
```
