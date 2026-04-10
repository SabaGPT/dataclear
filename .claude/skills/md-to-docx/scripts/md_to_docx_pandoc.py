#!/usr/bin/env python3
"""
Use Pandoc to convert Markdown to DOCX.

Auto-handled:
1) # / ## / ### -> Heading 1 / 2 / 3
2) ![](images/x.png) -> embedded images in DOCX
3) Markdown tables -> native Word tables
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def normalize_headings(md_text: str) -> str:
    """
    Ensure there is a space after ATX heading marks.
    Example: "##标题" -> "## 标题"
    """
    pattern = re.compile(r"^(#{1,6})([^\s#].*)$", re.MULTILINE)
    return pattern.sub(r"\1 \2", md_text)


def convert_markdown_to_docx(
    input_md: Path,
    output_docx: Path,
    reference_doc: Path | None = None,
    resource_path: str = ".",
) -> None:
    if shutil.which("pandoc") is None:
        raise RuntimeError(
            "未找到 pandoc。请先安装后再运行：\n"
            "Windows: winget install --id JohnMacFarlane.Pandoc -e"
        )

    if not input_md.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_md}")

    source_text = input_md.read_text(encoding="utf-8")
    normalized_text = normalize_headings(source_text)

    tmp_md = input_md.with_suffix(".normalized.tmp.md")
    tmp_md.write_text(normalized_text, encoding="utf-8")

    try:
        cmd = [
            "pandoc",
            str(tmp_md),
            "-o",
            str(output_docx),
            "--from=markdown+pipe_tables+grid_tables+multiline_tables",
            f"--resource-path={resource_path}",
            "--standalone",
        ]

        # Optional: apply custom Word styles if user has a reference docx.
        if reference_doc is not None:
            cmd.append(f"--reference-doc={reference_doc}")

        subprocess.run(cmd, check=True)
    finally:
        if tmp_md.exists():
            tmp_md.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Markdown file to DOCX with Pandoc."
    )
    parser.add_argument("input_md", type=Path, help="Input markdown file path")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output docx file path (default: same name as input)",
    )
    parser.add_argument(
        "--reference-doc",
        type=Path,
        default=None,
        help="Optional reference .docx for custom Word styles",
    )
    parser.add_argument(
        "--resource-path",
        default=".",
        help="Pandoc resource search path (default: .)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_md: Path = args.input_md

    if args.output is None:
        output_docx = input_md.with_suffix(".docx")
    else:
        output_docx = args.output

    try:
        convert_markdown_to_docx(input_md, output_docx, args.reference_doc, args.resource_path)
    except Exception as e:  # noqa: BLE001 - beginner-friendly CLI output
        print(f"[ERROR] {e}")
        return 1

    print(f"[OK] 转换完成: {output_docx}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
