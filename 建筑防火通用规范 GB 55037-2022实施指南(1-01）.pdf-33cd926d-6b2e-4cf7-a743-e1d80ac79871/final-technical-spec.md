# 建筑规范文档清洗技术方案（终版）

## 目标

建筑规范PDF → ima可入库的结构化docx（图文完整、表格可检索、零OCR错字）。

## Pipeline

```
PDF → MinerU解析 → Markdown + images/ → 预处理 → pandoc → clean.docx → ima入库
```

三步命令：

```bash
# Step 1: MinerU解析PDF
mineru input.pdf -o ./parsed/

# Step 2: 预处理（HTML表格转Markdown表格）
python fix_mineru_md.py ./parsed/input.md -o fixed.md

# Step 3: pandoc转docx
cd ./parsed/ && pandoc ../fixed.md -o clean.docx
```

## 每一步做了什么

### Step 1: MinerU解析

MinerU（opendatalab/MinerU，54.6k stars）用VLM+OCR双引擎解析PDF。

输入：source.pdf
输出：
```
parsed/
├── source.md        # 结构化Markdown
└── images/          # 提取的图片（hash命名.jpg）
```

MinerU自动完成：
- 文字识别（VLM+OCR双引擎，错误率远低于WPS）
- 去页眉、页脚、页码
- 保持阅读顺序和文档结构
- 标题检测为 `#` heading
- 图片导出到images/目录，Markdown中引用 `![](images/hash.jpg)`
- 表格导出为HTML `<table>` 标签
- 公式导出为LaTeX `$...$` 和 `$$...$$`

### Step 2: 预处理 fix_mineru_md.py

MinerU输出的表格是HTML `<table>` 标签，pandoc的Markdown reader不解析HTML表格为docx原生表格。预处理脚本用正则将HTML表格转为Markdown表格语法。

转换前：
```html
<table><tr><td>物质名称</td><td>最小点火能量</td></tr><tr><td>甲烷</td><td>0.470</td></tr></table>
```

转换后：
```markdown
| 物质名称 | 最小点火能量 |
| --- | --- |
| 甲烷 | 0.470 |
```

脚本50行，核心逻辑1个正则替换。

### Step 3: pandoc转docx

pandoc自动完成：
- `#` → Heading 1样式（ima按此切chunk）
- `![](images/x.jpg)` → docx内嵌图片（ima可召回）
- Markdown表格 → docx原生Table对象（ima可提取数值）
- `**加粗**` → Word Bold格式
- LaTeX公式 → 保留为文本（ima可文本检索）

可选：`--reference-doc=template.docx` 控制字体、间距等样式。

## 实测验证数据

### OCR质量对比（1-03文档，73页）

| 错误类型 | WPS转换 | MinerU |
|---------|---------|--------|
| 千→于（"对千""不低千"） | 几十处 | 0 |
| 矿→m²（面积单位） | 多处 | 0（"矿物棉"全部正确） |
| =隙→缝隙 | 多处 | 0（22处全部正确） |
| 方怯/倩形/烟囡/防姆 | 多处 | 0 |
| 公式 | 乱码 | 完整LaTeX |
| Ⅱ级/Ⅲ级 | Il级/川级 | Ⅱ级/Ⅲ级（正确罗马数字） |

结论：MinerU零OCR错误，不需要OCR扫描和人工校对。

### 图片（1-03文档）

- MinerU提取：29张图片
- pandoc嵌入docx：自动，`![](images/hash.jpg)` → docx内嵌

### 表格（1-01文档）

- MinerU输出：9个HTML表格
- 预处理后pandoc转换：9个docx原生表格，结构完整
- 验证：表2-1（14行×4列，物质名称+点火能量）数值全部正确

### Heading结构

MinerU将所有视觉突出行输出为 `#`（H1），包括：
```
# 6 建筑构造与装修        ← 章标题
# 6.1 防火墙              ← 节标题
# 【条文要点】            ← 注释标记
# 【实施要点】            ← 注释标记
```

pandoc全部转为Heading 1。效果：ima切chunk更碎，每个条文要点/实施要点独立成chunk。检索精度可能反而更高（每块更聚焦）。

如果ima验证发现chunk过碎影响检索，可加lua filter校正层级（约20行，按编号模式区分章/节/条文）。当前先不做，等ima实测结果。

## 批量处理

```bash
./batch_convert.sh ./parsed_dir/ ./output_dir/

# 带样式模板
./batch_convert.sh ./parsed_dir/ ./output_dir/ --template template.docx
```

batch_convert.sh 对目录下所有.md文件执行Step 2 + Step 3。

## 文件清单

```
gb-doc-cleaner/
├── fix_mineru_md.py      # 预处理脚本（50行）
├── batch_convert.sh      # 批量转换脚本
└── template.docx         # pandoc样式模板（可选，做一次复用）
```

## 依赖

| 工具 | 安装 | 用途 |
|------|------|------|
| MinerU | `pip install -U "mineru[all]"` | PDF解析 |
| pandoc | `brew install pandoc` 或 `apt install pandoc` | Markdown→docx |
| Python 3.8+ | 系统自带 | 预处理脚本 |

无Python第三方库依赖。fix_mineru_md.py只用标准库re和pathlib。

## 与旧方案对比

| 维度 | WPS路线（旧） | MinerU路线（新） |
|------|-------------|----------------|
| 步骤数 | 6步 | 3步 |
| 自定义脚本 | 3个（clean_standard + ocr_scanner + pdf_figure_extractor） | 1个（fix_mineru_md.py，50行） |
| 人工介入 | OCR替换清单确认 + Word查找替换 | 无 |
| OCR错误 | 几十处/文档 | 0 |
| 图片处理 | PyMuPDF从PDF截图 → 手动插入docx | MinerU自动导出 → pandoc自动嵌入 |
| 表格处理 | WPS转换后结构可能散架 | MinerU提取 → 预处理 → docx原生表格 |
| 公式处理 | 无（乱码） | LaTeX文本保留 |

## 待ima验证项

以下需要上传clean.docx到ima后确认：

| 验证项 | 预期 | 风险 |
|--------|------|------|
| chunk边界是否在Heading处 | 是（pandoc输出标准Heading样式） | 低 |
| 图片是否可召回 | 是（pandoc嵌入的图片与python-docx嵌入的结构相同） | 中——未实测pandoc的blip结构 |
| 表格数值是否可检索 | 是（docx原生表格，ima已验证可解析） | 低 |
| chunk粒度是否合适 | 可能偏碎（所有#都是H1） | 低——碎chunk检索精度可能更高 |

**单一最高ROI动作：拿一份clean.docx上传ima，跑检索测试。**
