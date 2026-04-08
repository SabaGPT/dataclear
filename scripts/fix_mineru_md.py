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
    """将HTML <table> 转换为Markdown表格语法，正确处理rowspan/colspan"""
    html = match.group(0)
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
    if not rows:
        return match.group(0)

    # 第1步：解析为二维网格，处理rowspan/colspan
    grid = []  # grid[row][col] = cell_text
    for r_idx, row_html in enumerate(rows):
        # 确保grid有足够的行
        while len(grid) <= r_idx:
            grid.append([])
        cells = re.finditer(r'<td(?P<attrs>[^>]*)>(?P<text>.*?)</td>', row_html, re.DOTALL)
        col = 0
        for cell in cells:
            attrs = cell.group('attrs')
            text = cell.group('text').strip()
            # 解析rowspan/colspan
            rs = int(m.group(1)) if (m := re.search(r'rowspan="(\d+)"', attrs)) else 1
            cs = int(m.group(1)) if (m := re.search(r'colspan="(\d+)"', attrs)) else 1
            # 跳过已被前面rowspan占据的列
            while col < len(grid[r_idx]) and grid[r_idx][col] is not None:
                col += 1
            # 填充rowspan × colspan区域
            for dr in range(rs):
                while len(grid) <= r_idx + dr:
                    grid.append([])
                for dc in range(cs):
                    target_col = col + dc
                    row_list = grid[r_idx + dr]
                    while len(row_list) <= target_col:
                        row_list.append(None)
                    # 首格放文本，合并区域其余格留空
                    row_list[target_col] = text if (dr == 0 and dc == 0) else ''
            col += cs

    # 第2步：统一列数
    max_cols = max(len(r) for r in grid) if grid else 0
    for row in grid:
        while len(row) < max_cols:
            row.append('')
        for i in range(len(row)):
            if row[i] is None:
                row[i] = ''

    # 第3步：生成Markdown表格
    md_rows = []
    for i, row in enumerate(grid):
        md_rows.append('| ' + ' | '.join(row) + ' |')
        if i == 0:
            md_rows.append('| ' + ' | '.join(['---'] * max_cols) + ' |')
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
