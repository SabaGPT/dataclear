#!/usr/bin/env python3
"""
md_to_pptx.py — Markdown → PPTX 转换 (入口脚本)

实际实现位于 .claude/skills/md-to-pptx/scripts/md_to_pptx.py
本文件为便捷入口，保持 scripts/ 目录的 CLI 一致性。

用法:
    python scripts/md_to_pptx.py input.md -o output.pptx --resource-path=./images_dir
"""

import subprocess
import sys
from pathlib import Path

_skill_script = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "md-to-pptx" / "scripts" / "md_to_pptx.py"

if not _skill_script.exists():
    print(f"[ERROR] Skill 脚本未找到: {_skill_script}", file=sys.stderr)
    print("请确认 .claude/skills/md-to-pptx/ 目录完整。", file=sys.stderr)
    sys.exit(1)

sys.exit(subprocess.call([sys.executable, str(_skill_script)] + sys.argv[1:]))
