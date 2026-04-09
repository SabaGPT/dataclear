# md-to-pptx — Markdown → PowerPoint Skill

将 Markdown 文件转换为结构化 PowerPoint 演示文稿。

设计风格参考 [baoyu-slide-deck](https://github.com/JimLiu/baoyu-skills)（corporate 风格）：
16:9 宽屏、深蓝标题栏、专业中文排版、自动内容拆分。

## 安装

### 方法 1：手动安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/SabaGPT/dataclear.git

# 复制 skill 到 Claude Code 全局目录
cp -r dataclear/.claude/skills/md-to-pptx ~/.claude/skills/

# 安装 Python 依赖
pip install python-pptx
```

### 方法 2：仅项目内使用

将 `.claude/skills/md-to-pptx/` 目录放入你项目的 `.claude/skills/` 下即可。

### 方法 3：Plugin Marketplace

```
/plugin marketplace add SabaGPT/dataclear
```

## 使用

### 在 Claude Code 中

直接对 Claude 说：
- "把这个 markdown 转成 PPT"
- "做PPT"
- "convert to pptx"
- `/md-to-pptx`

### 命令行直接调用

```bash
python ~/.claude/skills/md-to-pptx/scripts/md_to_pptx.py input.md -o output.pptx

# 带图片目录
python ~/.claude/skills/md-to-pptx/scripts/md_to_pptx.py input.md \
  -o output.pptx --resource-path=./images
```

## 功能

| 输入 | 输出 |
|------|------|
| `# H1`（首个） | 封面页：深蓝背景、居中大标题 |
| `# H1`（后续） | 章节分隔页：白底深蓝色带 |
| `## H2` / `### H3` | 内容页：深蓝标题栏 + 正文 |
| 段落文字 | 正文，超长自动拆分多页 |
| Pipe 表格 | 原生 PPTX 表格，超 10 行自动分页 |
| `![](path)` | 图片页：居中最大化显示 |
| 列表 | 正文文字 |

## 设计风格

- **布局**: 16:9 宽屏
- **配色**: 白底 + 深蓝(#1E3A5F) + 蓝色强调(#2B6CB0)
- **字体**: Microsoft YaHei（标题粗体 24-36pt，正文 16pt）
- **规则**: 无页脚页码、大量留白、每页一主题

## 文件结构

```
md-to-pptx/
├── SKILL.md                    # Skill 定义（触发词、工作流、架构图）
├── scripts/
│   └── md_to_pptx.py          # 转换引擎（Python, ~620行）
└── references/
    ├── design-style.md         # 配色、字体、布局规格
    └── content-rules.md        # 内容拆分和映射规则
```

## 依赖

- Python 3.8+
- `python-pptx`（`pip install python-pptx`）
- `Pillow`（随 python-pptx 自动安装，用于图片嵌入）

## 许可

MIT
