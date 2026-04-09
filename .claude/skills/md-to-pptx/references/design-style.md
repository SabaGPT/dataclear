# Design Style Reference — Corporate

Based on baoyu-slide-deck corporate preset. Designed for professional documents,
standards, and technical content.

## Color Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Navy | #1E3A5F | (30, 58, 95) | Title bars, cover background, table headers |
| Accent Blue | #2B6CB0 | (43, 108, 176) | Accent lines, highlights, links |
| White | #FFFFFF | (255, 255, 255) | Slide background, title text on dark |
| Dark Gray | #2D2D2D | (45, 45, 45) | Body text |
| Light Gray BG | #F3F4F6 | (243, 244, 246) | Subtitle text, secondary backgrounds |
| Table Alt Row | #EBEFF5 | (235, 239, 245) | Alternating table row background |

## Typography

### Font Families

| Purpose | Chinese | Latin Fallback |
|---------|---------|---------------|
| Title | Microsoft YaHei Bold | Arial Bold |
| Body | Microsoft YaHei | Arial |
| Table | Microsoft YaHei | Arial |

### Font Sizes

| Element | Size | Weight |
|---------|------|--------|
| Cover title | 36pt | Bold |
| Cover subtitle | 18pt | Regular |
| Section divider title | 32pt | Bold |
| Slide title (title bar) | 24pt | Bold |
| Body text | 16pt | Regular |
| Table header | 13pt | Bold |
| Table body | 12pt | Regular |

## Layout Specifications

### Slide Dimensions

- **Aspect ratio**: 16:9 widescreen
- **Width**: 13.333 inches (33.867 cm)
- **Height**: 7.5 inches (19.05 cm)

### Margins

| Edge | Size |
|------|------|
| Left | 0.8 in |
| Right | 0.8 in |
| Top | 0.6 in |
| Bottom | 0.5 in |

### Title Bar

- **Height**: 1.0 inch
- **Background**: Navy (#1E3A5F)
- **Text**: White, left-aligned, 24pt bold
- **Text inset**: 0.15 in from top

### Body Area

- **Top**: Title bar bottom + 0.2 in gap
- **Width**: Slide width - left margin - right margin
- **Height**: Slide height - body top - bottom margin

## Slide Layouts

### 1. Cover (封面)

- Full-slide navy background
- Centered title: 36pt bold white, vertically at ~24% from top
- Accent line: blue (#2B6CB0), 0.06 in height, centered at ~45% from top
- Optional subtitle: 18pt light gray, below accent line

### 2. Section Divider (章节分隔)

- White background with navy band: 3.0 in height, vertically centered at ~29% from top
- Section title: 32pt bold white, centered within band

### 3. Content (内容)

- Navy title bar at top
- Body text area below
- Line spacing: 6pt after each paragraph
- Text wraps automatically

### 4. Table (表格)

- Navy title bar at top
- Native PPTX table fills body area
- Header row: navy background, white bold text
- Body rows: alternating white / light blue-gray
- Cell text: vertically centered

### 5. Image (图片)

- Navy title bar at top
- Image centered and maximized in body area
- Maintains original aspect ratio
- Missing images show placeholder text in blue

## Design Principles (from baoyu-slide-deck)

1. **One idea per slide** — avoid cramming multiple topics
2. **No footers, page numbers, or logos** — clean visual space
3. **Generous whitespace** — minimum 10% margin from all edges
4. **Consistent visual language** — same colors, fonts, spacing throughout
5. **Content density control** — max ~12 lines or ~400 chars per slide
6. **Narrative headlines** — use descriptive titles, not generic labels
7. **Direct tone** — confident, professional; avoid filler words
