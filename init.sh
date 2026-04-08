#!/usr/bin/env bash
# init.sh — 初始化数据目录结构（克隆仓库后运行一次）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data/documents"

DOCS=(
    "DB32／T+5183-2025+地下民用建筑防火设计标准"
    "建筑防火通用规范 GB 55037-2022实施指南(1-01）"
    "建筑防火通用规范 GB 55037-2022实施指南(1-02)"
    "建筑防火通用规范 GB 55037-2022实施指南(1-03)"
    "建筑防火通用规范 GB 55037-2022实施指南(1-04)"
    "建筑防火通用规范 GB 55037-2022实施指南(1-05)"
    "GB+35181-2025"
    "《教育系统重大事故隐患判定指南》"
    "浙江省消防技术规范难点问题操作技术指南（2025版）"
)

echo "初始化数据目录..."

for doc in "${DOCS[@]}"; do
    mkdir -p "$DATA_DIR/$doc"/{source,mineru_output,output}
    echo "  [OK] $doc"
done

echo "=========="
echo "完成。请将 MinerU 输出的 .md 和 images/ 放入对应的 mineru_output/ 目录。"
echo "然后运行: bash process_all.sh"
