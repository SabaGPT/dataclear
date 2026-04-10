#!/usr/bin/env python3
"""
md_to_docx_pandoc.py — Markdown → DOCX 转换 (入口脚本)

实际实现位于 .claude/skills/md-to-docx/scripts/md_to_docx_pandoc.py
本文件为便捷入口，保持 scripts/ 目录的 CLI 一致性。

用法:
    python scripts/md_to_docx_pandoc.py input.md -o output.docx --resource-path=mineru_output
"""

import subprocess
import sys
from pathlib import Path

_skill_script = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "md-to-docx" / "scripts" / "md_to_docx_pandoc.py"

if not _skill_script.exists():
    print(f"[ERROR] Skill 脚本未找到: {_skill_script}", file=sys.stderr)
    print("请确认 .claude/skills/md-to-docx/ 目录完整。", file=sys.stderr)
    sys.exit(1)

sys.exit(subprocess.call([sys.executable, str(_skill_script)] + sys.argv[1:]))
