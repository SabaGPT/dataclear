---
name: md-to-pptx
description: >
  Convert Markdown files to structured PowerPoint presentations (PPTX).
  Trigger when: user says "make PPT", "create slides", "convert to pptx",
  "markdown to PowerPoint", "生成PPT", "做PPT", "转PPT", or references
  creating presentations from markdown content.
  Supports Chinese content, pipe tables, images, and automatic content splitting.
---

# Markdown to PPTX Converter

Convert Markdown files into professional, structured PowerPoint presentations.
Design inspired by baoyu-slide-deck corporate style: clean 16:9 layout, navy title bars, professional typography.

## Prerequisites

Ensure `python-pptx` is installed:
```bash
pip install python-pptx
```

## Workflow

### Step 1: Identify Input

Determine the Markdown file to convert. Accept one of:
- A file path provided by the user
- Markdown content pasted by the user (save to a temp file first)
- A document directory path (look for `output/fixed.md` inside it)

If the user provides a document directory (e.g. `data/documents/GB+35181-2025`), the input is `<dir>/output/fixed.md` and `--resource-path` should be `<dir>/mineru_output`.

If the input markdown contains HTML `<table>` tags, suggest running `fix_mineru_md.py` first:
```bash
python scripts/fix_mineru_md.py input.md -o preprocessed.md
```

### Step 2: Run Conversion

Use the project's conversion script:

```bash
python scripts/md_to_pptx.py <input.md> -o <output.pptx> --resource-path=<images_dir>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `input.md` | Yes | Input Markdown file |
| `-o, --output` | No | Output .pptx path (default: same name as input) |
| `--resource-path` | No | Directory to resolve image paths (default: `.`) |

**Example for dataclear documents:**
```bash
python scripts/md_to_pptx.py data/documents/GB+35181-2025/output/fixed.md \
  -o data/documents/GB+35181-2025/output/clean.pptx \
  --resource-path=data/documents/GB+35181-2025/mineru_output
```

### Step 3: Report Results

After successful conversion, report:
- Output file path
- Number of slides generated
- File size

If conversion fails, check:
1. `python-pptx` is installed (`pip install python-pptx`)
2. Input file exists and is valid Markdown
3. Image paths are resolvable from `--resource-path`

## Supported Markdown Elements

| Element | PPTX Result |
|---------|-------------|
| `# H1` (first) | Cover slide with large centered title |
| `# H1` (others) | Section divider slide |
| `## H2` / `### H3` | Content slide with title bar |
| Paragraphs | Body text, auto-split if too long |
| Pipe tables | Native PPTX tables, auto-split if >10 rows |
| `![](path)` | Full-slide image, centered and maximized |
| Lists (`-` / `1.`) | Body text with list items |

## Design Style

- **Layout**: 16:9 widescreen
- **Colors**: White background, navy (#1E3A5F) title bars, blue (#2B6CB0) accents
- **Fonts**: Microsoft YaHei (titles bold 24-36pt, body 16pt, tables 12pt)
- **Rules**: No footers, no page numbers, generous margins (10%+)
- **Content density**: Max ~12 lines or ~400 chars per slide, auto-split with "(续)" labels

## Batch Processing

To convert all documents in the dataclear pipeline:
```bash
for doc_dir in data/documents/*/; do
  fixed="$doc_dir/output/fixed.md"
  if [ -f "$fixed" ]; then
    python scripts/md_to_pptx.py "$fixed" \
      -o "$doc_dir/output/clean.pptx" \
      --resource-path="$doc_dir/mineru_output"
  fi
done
```
