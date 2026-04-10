#!/usr/bin/env python3
"""
extract_style.py — 从品牌 PPTX 逆向工程提取风格配置

从现有 .pptx 文件中提取颜色主题、字体、尺寸等信息，
生成 JSON 配置文件，可直接用于 md_to_pptx.py --style-file=

用法:
    python extract_style.py brand.pptx -o brand_style.json
    python md_to_pptx.py input.md --style-file=brand_style.json
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


DRAWINGML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def _parse_color_element(el) -> str | None:
    """Extract hex color from a theme color element."""
    srgb = el.find(f"{{{DRAWINGML_NS}}}srgbClr")
    if srgb is not None:
        return f"#{srgb.get('val', '000000')}"
    sys_clr = el.find(f"{{{DRAWINGML_NS}}}sysClr")
    if sys_clr is not None:
        return f"#{sys_clr.get('lastClr', '000000')}"
    return None


def extract_theme_from_pptx(pptx_path: str) -> dict:
    """Extract theme colors and fonts from a .pptx file."""
    result = {
        "source": Path(pptx_path).name,
        "colors": {},
        "fonts": {},
        "slide_width": None,
        "slide_height": None,
    }

    with zipfile.ZipFile(pptx_path, "r") as zf:
        # ── Parse theme XML ──
        theme_files = [n for n in zf.namelist() if "theme" in n.lower() and n.endswith(".xml")]
        if theme_files:
            theme_xml = zf.read(theme_files[0])
            root = ET.fromstring(theme_xml)

            # Color scheme
            clr_scheme = root.find(f".//{{{DRAWINGML_NS}}}clrScheme")
            if clr_scheme is not None:
                color_map = {
                    "dk1": "dark1", "dk2": "dark2",
                    "lt1": "light1", "lt2": "light2",
                    "accent1": "accent1", "accent2": "accent2",
                    "accent3": "accent3", "accent4": "accent4",
                    "accent5": "accent5", "accent6": "accent6",
                    "hlink": "hyperlink", "folHlink": "followed_hyperlink",
                }
                for xml_name, json_name in color_map.items():
                    el = clr_scheme.find(f"{{{DRAWINGML_NS}}}{xml_name}")
                    if el is not None:
                        color = _parse_color_element(el)
                        if color:
                            result["colors"][json_name] = color

            # Font scheme
            font_scheme = root.find(f".//{{{DRAWINGML_NS}}}fontScheme")
            if font_scheme is not None:
                for font_type in ("majorFont", "minorFont"):
                    font_el = font_scheme.find(f"{{{DRAWINGML_NS}}}{font_type}")
                    if font_el is not None:
                        latin = font_el.find(f"{{{DRAWINGML_NS}}}latin")
                        ea = font_el.find(f"{{{DRAWINGML_NS}}}ea")
                        key = "major" if "major" in font_type else "minor"
                        if latin is not None:
                            result["fonts"][f"{key}_latin"] = latin.get("typeface", "")
                        if ea is not None:
                            result["fonts"][f"{key}_east_asian"] = ea.get("typeface", "")

        # ── Parse presentation.xml for slide dimensions ──
        if "ppt/presentation.xml" in zf.namelist():
            pres_xml = zf.read("ppt/presentation.xml")
            pres_root = ET.fromstring(pres_xml)
            pres_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
            sld_sz = pres_root.find(f"{{{pres_ns}}}sldSz")
            if sld_sz is not None:
                cx = int(sld_sz.get("cx", 0))
                cy = int(sld_sz.get("cy", 0))
                if cx and cy:
                    result["slide_width"] = round(cx / 914400, 3)
                    result["slide_height"] = round(cy / 914400, 3)

    return result


def theme_to_style_config(theme: dict) -> dict:
    """Convert extracted theme to a md_to_pptx StyleConfig JSON."""
    colors = theme.get("colors", {})
    fonts = theme.get("fonts", {})

    style = {
        "name": Path(theme.get("source", "custom")).stem,
        "title_bg": colors.get("dark1", colors.get("accent1", "#1E3A5F")),
        "accent": colors.get("accent1", colors.get("accent2", "#2B6CB0")),
        "text_color": colors.get("dark1", "#2D2D2D"),
        "bg_color": colors.get("light1", "#FFFFFF"),
        "light_bg": colors.get("light2", "#F3F4F6"),
        "table_header": colors.get("dark1", colors.get("accent1", "#1E3A5F")),
        "table_alt": colors.get("light2", "#EBEFF5"),
        "font_title": fonts.get("major_east_asian") or fonts.get("major_latin", "Microsoft YaHei"),
        "font_body": fonts.get("minor_east_asian") or fonts.get("minor_latin", "Microsoft YaHei"),
    }

    return style


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract style from branded PPTX for md_to_pptx.py"
    )
    parser.add_argument("pptx_file", help="Input .pptx file to analyze")
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output JSON file (default: <input>_style.json)",
    )
    parser.add_argument(
        "--raw", action="store_true",
        help="Output raw theme data instead of StyleConfig format",
    )
    args = parser.parse_args()

    pptx_path = args.pptx_file
    if not Path(pptx_path).exists():
        print(f"[ERROR] 文件不存在: {pptx_path}")
        return 1

    try:
        theme = extract_theme_from_pptx(pptx_path)
    except Exception as e:
        print(f"[ERROR] 解析失败: {e}")
        return 1

    if args.raw:
        output_data = theme
    else:
        output_data = theme_to_style_config(theme)

    output_path = args.output or Path(pptx_path).stem + "_style.json"
    Path(output_path).write_text(
        json.dumps(output_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"[OK] 风格提取完成: {output_path}")
    print(f"  来源: {theme.get('source', '?')}")
    if not args.raw:
        print(f"  主色: {output_data['title_bg']}")
        print(f"  强调色: {output_data['accent']}")
        print(f"  标题字体: {output_data['font_title']}")
        print(f"  正文字体: {output_data['font_body']}")
    print(f"\n使用: python md_to_pptx.py input.md --style-file={output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
