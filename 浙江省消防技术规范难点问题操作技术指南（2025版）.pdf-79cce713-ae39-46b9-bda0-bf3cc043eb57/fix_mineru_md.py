#!/usr/bin/env python3
"""
fix_mineru_md.py — MinerU Markdown预处理，修复pandoc不兼容的格式

用法:
    python fix_mineru_md.py input.md -o output.md
    python fix_mineru_md.py ./dir/ --batch -o ./fixed/

做两件事:
1. HTML <table> → Markdown表格（pandoc markdown reader不解析HTML表格）
2. （预留）heading层级校正（如果ima需要）
"""

import re
import argparse
from pathlib import Path


def html_table_to_markdown(match):
    """将HTML <table> 转换为Markdown表格语法"""
    html = match.group(0)
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
    md_rows = []
    for i, row in enumerate(rows):
        cells = re.findall(r'<td(?:\s[^>]*)?>(.*?)</td>', row, re.DOTALL)
        cells = [c.strip() for c in cells]
        if not cells:
            continue
        md_rows.append('| ' + ' | '.join(cells) + ' |')
        if i == 0:
            md_rows.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
    return '\n'.join(md_rows)


def fix_markdown(content):
    """预处理MinerU输出的Markdown"""
    # 1. HTML tables → Markdown tables
    content = re.sub(r'<table>.*?</table>', html_table_to_markdown, content, flags=re.DOTALL)
    
    return content


def main():
    parser = argparse.ArgumentParser(description='MinerU Markdown预处理')
    parser.add_argument('input', help='Markdown文件或目录')
    parser.add_argument('-o', '--output', required=True, help='输出文件或目录')
    parser.add_argument('--batch', action='store_true', help='批量处理目录')
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if args.batch:
        output_path.mkdir(parents=True, exist_ok=True)
        md_files = sorted(input_path.glob('**/*.md'))
        for md in md_files:
            content = md.read_text(encoding='utf-8')
            fixed = fix_markdown(content)
            out = output_path / md.name
            out.write_text(fixed, encoding='utf-8')
            
            # Count fixes
            html_tables = len(re.findall(r'<table>', content))
            print(f"  {md.name}: {html_tables} HTML tables converted")
        print(f"Done. {len(md_files)} files processed.")
    else:
        content = input_path.read_text(encoding='utf-8')
        html_tables = len(re.findall(r'<table>', content))
        fixed = fix_markdown(content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(fixed, encoding='utf-8')
        print(f"{input_path.name}: {html_tables} HTML tables converted -> {output_path}")


if __name__ == '__main__':
    main()
