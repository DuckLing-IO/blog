# md2html

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

> *[English Version](./README_EN.md)*

一款轻量级的 Markdown 转 HTML 工具，专为个人博客设计。将单篇 `.md` 文件转换为自包含、精美排版的 HTML 页面，无需静态站点生成器。

---

## 功能特性

- **单文件转换** — 指定一篇 `.md`，产出一篇 `.html`
- **完全自包含** — CSS 全部内联，字体通过 Google Fonts 加载，无外部依赖
- **默认暗色主题** — 黑色背景，Poppins 标题字体，Lora 正文字体
- **VS Code 风格代码块** — Pygments 语法高亮（支持 monokai / nord / material 等多种主题），语言标签，圆角容器
- **自动时间戳** — 标题右侧自动附带生成时间，格式为 `yyyy-mm-dd HH:MM 星期X`
- **本地图片支持** — 自动复制与 `.md` 同名的图片文件夹到输出目录，并修正引用路径
- **版权脚注** — 可配置的版权信息，支持超链接
- **YAML 配置文件** — 字体、颜色、代码主题、输出路径……无需修改代码即可自定义
- **GUI + CLI 双模式** — 双击 `md2html-gui.exe` 或命令行运行皆可

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 命令行转换

```bash
python md2html.py my_post.md
```

转换后的 HTML 保存在 `./output/my_post.html`。

### 3. 图形界面

```bash
python gui.py
```

Windows 用户可直接双击 `md2html-gui.exe`。

---

## 命令行用法

```
python md2html.py <输入文件.md> [选项]
```

| 参数 | 说明 |
|------|------|
| `input` | Markdown 文件路径 |
| `-o, --output` | 输出 HTML 路径（默认: `./output/<文件名>.html`） |
| `-c, --config` | 配置文件路径（默认: `config.yaml`） |

**示例：**

```bash
# 基本转换
python md2html.py post.md

# 指定输出路径
python md2html.py post.md -o blog/my-post.html

# 使用自定义配置
python md2html.py post.md -c my_theme.yaml
```

---

## 图形界面用法

启动 GUI：

```bash
python gui.py
# Windows 用户可直接双击 md2html-gui.exe
```

1. 点击 **浏览…** 选择你的 Markdown 文件
2. 输出路径会自动填充（可手动修改）
3. 点击 **开始转换**
4. 在日志区域查看转换进度与结果路径

---

## 配置文件

编辑脚本 / exe 同目录下的 `config.yaml`。所有键均可省略，省略项自动回退到内置默认值。

```yaml
output:
  default_dir: "./output"          # 默认输出目录

styles:
  title:
    font: "Poppins"                # 一级标题字体（Google Fonts 自动加载）
    size: "2em"                    # 字号
    weight: "700"                  # 粗细: 400/600/700
  heading:
    font: "Poppins"                # 其余标题 (h2–h6) 共用字体
  body:
    font: "Lora"                   # 正文字体（中文回退到 Noto Serif SC）
    size: "16px"                   # 基础字号
    line_height: "1.8"             # 行高倍率
  background_color: "#000000"      # 页面背景色
  text_color:       "#e0e0e0"      # 正文文字色
  link_color:       "#6ea8fe"      # 超链接色
  max_width: "800px"               # 内容最大宽度

code:
  theme: "monokai"                 # Pygments 高亮主题
  show_line_numbers: false         # 是否显示行号
  border_radius: 8                 # 代码容器圆角（px）
  background: "#1e1e1e"            # 代码区域背景色

footer:
  text: "© 2025 - 2026 By DuckLing"   # 版权文字
  link_url: "https://duckee.top"       # 超链接目标
  link_text: "DuckLing"                # 转为超链接的文字（留空则不生成链接）

meta:
  lang: "zh-CN"                    # 页面语言（影响星期显示）
  viewport: "width=device-width, initial-scale=1.0"
```

> 全部 Pygments 主题列表见 [Pygments Styles](https://pygments.org/styles/)。

---

## 本地图片说明

如果 Markdown 中引用了本地图片，请将它们放入**与 `.md` 文件同名的文件夹**（不含扩展名）：

```
blog/
├── my_post.md          # 文中引用了 photo.jpg 和 screenshot.png
├── my_post/
│   ├── photo.jpg
│   └── screenshot.png
```

转换器会自动：

1. 将整个 `my_post/` 文件夹复制到输出 HTML 旁边
2. 将裸文件名引用（如 `photo.jpg`）修正为 `my_post/photo.jpg`

远程 URL 图片不受影响。

---

## 构建可执行文件

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "md2html-gui" \
  --hidden-import=pymdownx \
  --hidden-import=pymdownx.highlight \
  --hidden-import=pymdownx.superfences \
  gui.py
```

生成的 `.exe` 位于 `dist/` 目录。将 `config.yaml` 放在 exe 同目录下即可生效。

---

## 项目结构

```
md2html/
├── md2html.py           # 核心转换脚本（CLI）
├── gui.py               # 图形界面（tkinter）
├── md2html-gui.exe      # Windows 独立可执行文件
├── config.yaml          # 默认配置文件
├── requirements.txt     # Python 依赖
└── .gitignore
```

---

## 依赖项

| 包 | 版本 | 用途 |
|----|------|------|
| [markdown](https://python-markdown.github.io/) | ≥ 3.5 | Markdown 解析 |
| [pymdown-extensions](https://facelessuser.github.io/pymdown-extensions/) | ≥ 10.0 | 扩展 Markdown 语法 |
| [Pygments](https://pygments.org/) | ≥ 2.15 | 代码语法高亮 |
| [PyYAML](https://pyyaml.org/) | ≥ 6.0 | 配置文件解析 |

GUI：使用 Python 内置 `tkinter`，无需额外安装。

---

## 许可证

MIT
