#!/usr/bin/env bash
# run_test.sh — md-to-pptx skill 测试脚本
#
# 用法:
#   bash .claude/skills/md-to-pptx/tests/run_test.sh
#
# 测试内容:
#   1. 依赖检查 (python-pptx)
#   2. 基础转换 (demo.md → demo.pptx)
#   3. 输出验证 (幻灯片数量、布局类型统计)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONVERTER="$SKILL_DIR/scripts/md_to_pptx.py"
DEMO_MD="$SCRIPT_DIR/demo.md"
OUTPUT_PPTX="$SCRIPT_DIR/demo.pptx"
RESOURCE_PATH="$SCRIPT_DIR"

echo "═══════════════════════════════════════════"
echo "  md-to-pptx Skill 测试"
echo "═══════════════════════════════════════════"
echo ""

# ── Test 1: 依赖检查 ────────────────────────
echo "▸ Test 1: 检查依赖..."
if python3 -c "import pptx; print(f'  python-pptx {pptx.__version__}')" 2>/dev/null || \
   python -c "import pptx; print(f'  python-pptx {pptx.__version__}')" 2>/dev/null; then
    echo "  ✓ python-pptx 已安装"
else
    echo "  ✗ python-pptx 未安装"
    echo "  运行: pip install python-pptx"
    exit 1
fi

if python3 -c "from PIL import Image; print(f'  Pillow OK')" 2>/dev/null || \
   python -c "from PIL import Image; print(f'  Pillow OK')" 2>/dev/null; then
    echo "  ✓ Pillow 已安装"
else
    echo "  ⚠ Pillow 未安装（图片嵌入不可用）"
fi
echo ""

# ── Test 2: 转换 ─────────────────────────────
echo "▸ Test 2: 转换 demo.md → demo.pptx..."
echo "  输入: $DEMO_MD"

# 检测 python 命令
if python3 -c "pass" 2>/dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

$PYTHON "$CONVERTER" "$DEMO_MD" -o "$OUTPUT_PPTX" --resource-path="$RESOURCE_PATH"
echo ""

# ── Test 3: 验证输出 ──────────────────────────
echo "▸ Test 3: 验证输出..."
echo "  文件: $OUTPUT_PPTX"
echo "  大小: $(du -h "$OUTPUT_PPTX" | cut -f1)"

$PYTHON - "$OUTPUT_PPTX" << 'PYEOF'
import sys
from pptx import Presentation

pptx_path = sys.argv[1]
prs = Presentation(pptx_path)

total = len(prs.slides)
print(f"  幻灯片: {total} 张")

# Count layout types by analyzing shapes
covers = 0
sections = 0
tables = 0
images = 0
content = 0

for slide in prs.slides:
    has_table = any(s.has_table for s in slide.shapes)
    has_image = any(hasattr(s, 'image') and s.shape_type == 13 for s in slide.shapes)

    # Full-background shape = cover or section
    shapes = list(slide.shapes)
    full_bg = any(
        s.left == 0 and s.width == prs.slide_width and s.height == prs.slide_height
        for s in shapes if hasattr(s, 'left')
    )
    partial_band = any(
        s.left == 0 and s.width == prs.slide_width
        and s.height != prs.slide_height and s.height > 1000000  # > 1 inch
        and s.top > 1000000  # not at top (not title bar)
        for s in shapes if hasattr(s, 'left')
    )

    if full_bg:
        covers += 1
    elif partial_band:
        sections += 1
    elif has_table:
        tables += 1
    elif has_image:
        images += 1
    else:
        content += 1

print(f"  ├ 封面页:     {covers}")
print(f"  ├ 章节分隔页: {sections}")
print(f"  ├ 内容页:     {content}")
print(f"  ├ 表格页:     {tables}")
print(f"  └ 图片页:     {images}")

# Validate minimum expectations
assert total >= 15, f"幻灯片过少: {total} (期望 ≥15)"
assert covers >= 1, "缺少封面页"
assert tables >= 3, f"表格页过少: {tables} (期望 ≥3)"
assert images >= 1, f"图片页过少: {images} (期望 ≥1)"

print()
print("  ✓ 所有验证通过")
PYEOF

echo ""
echo "═══════════════════════════════════════════"
echo "  测试完成"
echo "═══════════════════════════════════════════"
echo ""
echo "用 PowerPoint/WPS/LibreOffice 打开查看:"
echo "  $OUTPUT_PPTX"
