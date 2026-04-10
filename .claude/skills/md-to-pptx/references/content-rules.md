# Content Rules

Rules for mapping Markdown content to PowerPoint slides.

## Heading → Slide Mapping

| Markdown | Slide Type | Notes |
|----------|-----------|-------|
| `# H1` (first) | Cover slide | Document title, centered large text |
| `# H1` (subsequent) | Section divider | Chapter break, centered on navy band |
| `## H2` | Content slide | Becomes slide title in title bar |
| `### H3` and below | Content slide | Same as H2, title in title bar |

## Content Splitting

When content under a heading exceeds slide capacity, it is split across multiple
slides. The second and subsequent slides append "(续N)" to the title.

### Thresholds

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Max body lines | 12 | Readable at presentation distance |
| Max body chars | 400 | ~200 CJK chars at 16pt fits body area |
| Max table rows | 10 | Header + 9 data rows per slide |

### Split Priority

1. **Paragraph boundary** — never break mid-paragraph
2. **Sentence boundary** (。！？) — if a single paragraph exceeds limits
3. **Character boundary** — last resort, should rarely happen

### CJK Character Width Estimation

For line-width estimation, CJK characters count as 2 units, Latin characters as 1.
A slide line holds approximately 80 units (~40 CJK chars or ~80 Latin chars at 16pt).

## Table Handling

| Condition | Action |
|-----------|--------|
| ≤10 rows | Single table slide |
| >10 rows | Split into chunks, repeat header row on each slide |
| ≤6 columns | Normal column width distribution |
| >6 columns | Consider reducing font size (future enhancement) |

Tables always get their own dedicated slide — never mixed with body text on the
same slide.

## Image Handling

| Condition | Action |
|-----------|--------|
| Image found | Dedicated image slide, centered, maximized with aspect ratio |
| Image not found | Placeholder text: "[图片未找到: path]" |

Images always get their own dedicated slide. The image is scaled to the maximum
size that fits within the body area while maintaining its original aspect ratio.

Resolution path: `--resource-path` directory first, then current working directory.

## List Handling

List items (`-`, `*`, `1.`) are treated as text content. Each item becomes a
line in the body text area. Lists follow the same splitting rules as paragraphs.

## Content Before Headings

Any content appearing before the first heading is treated as orphan content and
rendered as content slides with an empty title.
