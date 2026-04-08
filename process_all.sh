#!/usr/bin/env bash
# process_all.sh — 一键批处理所有文档
# 用法:
#   bash process_all.sh            # 处理所有文档
#   bash process_all.sh "文档名"   # 只处理指定文档

set -euo pipefail

# 自动检测python命令（Windows上python3可能是Store stub）
if python3 -c "pass" 2>/dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data/documents"

ok=0
fail=0
skip=0

for doc_dir in "$DATA_DIR"/*/; do
    name="$(basename "$doc_dir")"

    # 如果指定了文档名参数，只处理匹配的
    if [ -n "${1:-}" ] && [ "$name" != "$1" ]; then continue; fi

    # 查找源 markdown（优先级：MinerU_markdown_*.md > full.md > 任意 .md）
    src="$(find "$doc_dir/mineru_output" -maxdepth 1 -name "MinerU_markdown_*.md" -type f 2>/dev/null | head -1)"
    if [ -z "$src" ]; then
        src="$(find "$doc_dir/mineru_output" -maxdepth 1 -name "full.md" -type f 2>/dev/null | head -1)"
    fi
    if [ -z "$src" ]; then
        src="$(find "$doc_dir/mineru_output" -maxdepth 1 -name "*.md" -type f 2>/dev/null | head -1)"
    fi

    if [ -z "$src" ]; then
        echo "[SKIP] $name — mineru_output/ 中无 .md 文件"
        skip=$((skip + 1))
        continue
    fi

    mkdir -p "$doc_dir/output"

    echo "[处理] $name"
    echo "  源文件: $(basename "$src")"

    # Step 1: fix_mineru_md.py 预处理 → output/fixed.md
    $PYTHON "$SCRIPT_DIR/scripts/fix_mineru_md.py" "$src" -o "$doc_dir/output/fixed.md"

    # Step 2: md_to_docx_pandoc.py 转docx → output/clean.docx
    # 必须 cd 到文档目录，让 pandoc --resource-path=. 找到 mineru_output/images/
    if (cd "$doc_dir" && $PYTHON "$SCRIPT_DIR/scripts/md_to_docx_pandoc.py" output/fixed.md -o output/clean.docx --resource-path=mineru_output); then
        echo "  [OK] → output/clean.docx"
        ok=$((ok + 1))
    else
        echo "  [FAIL] 转换失败"
        fail=$((fail + 1))
    fi
done

echo "=========="
echo "处理完成: 成功 $ok / 失败 $fail / 跳过 $skip"
