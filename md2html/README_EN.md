# md2html

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

> *[中文版本](./README.md)*

A lightweight Markdown-to-HTML converter built for personal blogs. Converts a single `.md` file into a self-contained, beautifully styled HTML page — no static site generator needed.

---

## Features

- **Single-file conversion** — point at one `.md` file, get one `.html` page
- **Self-contained output** — all CSS inlined, fonts loaded from Google Fonts, no external dependencies
- **Dark theme by default** — black background, Poppins headings, Lora body text
- **VS Code–style code blocks** — Pygments syntax highlighting (monokai / nord / material / …), language label, rounded container
- **Auto timestamp** — generation time appended to the right of the title in `yyyy-mm-dd HH:MM 星期X` format
- **Local image support** — auto-copies the companion image folder (same stem as `.md`) next to the output
- **Copyright footer** — configurable footer with clickable link
- **YAML configuration** — fonts, colors, code theme, output path … all tweakable without touching code
- **GUI + CLI** — double-click `md2html-gui.exe` or run from terminal

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Convert a file (CLI)

```bash
python md2html.py my_post.md
```

The HTML will be saved to `./output/my_post.html`.

### 3. Or use the GUI

```bash
python gui.py
```

Or double-click `md2html-gui.exe` (Windows).

---

## CLI Usage

```
python md2html.py <input.md> [options]
```

| Argument | Description |
|----------|-------------|
| `input` | Path to the Markdown file |
| `-o, --output` | Output HTML path (default: `./output/<stem>.html`) |
| `-c, --config` | Path to config YAML (default: `config.yaml`) |

**Examples:**

```bash
# Basic conversion
python md2html.py post.md

# Custom output path
python md2html.py post.md -o blog/my-post.html

# Custom config
python md2html.py post.md -c my_theme.yaml
```

---

## GUI Usage

Launch the GUI:

```bash
python gui.py
# or double-click md2html-gui.exe on Windows
```

1. Click **浏览…** to select your Markdown file
2. The output path is auto-filled (editable)
3. Click **开始转换**
4. Check the log panel for progress and the result path

---

## Configuration

Edit `config.yaml` next to the script / exe. All keys are optional — omitted ones fall back to built-in defaults.

```yaml
output:
  default_dir: "./output"

styles:
  title:
    font: "Poppins"         # Google Fonts name
    size: "2em"
    weight: "700"
  heading:
    font: "Poppins"         # h2–h6 share this font
  body:
    font: "Lora"
    size: "16px"
    line_height: "1.8"
  background_color: "#000000"
  text_color:       "#e0e0e0"
  link_color:       "#6ea8fe"
  max_width: "800px"

code:
  theme: "monokai"           # Pygments theme
  show_line_numbers: false
  border_radius: 8           # px
  background: "#1e1e1e"

footer:
  text: "© 2025 - 2026 By DuckLing"
  link_url: "https://duckee.top"
  link_text: "DuckLing"     # which part becomes a hyperlink

meta:
  lang: "zh-CN"
  viewport: "width=device-width, initial-scale=1.0"
```

> For the full list of Pygments themes, see [Pygments Styles](https://pygments.org/styles/).

---

## Local Images

If your Markdown file references local images, place them in a folder **with the same name as the `.md` file** (without extension):

```
blog/
├── my_post.md          # references photo.jpg and screenshot.png
├── my_post/
│   ├── photo.jpg
│   └── screenshot.png
```

The converter will:

1. Copy the entire `my_post/` folder next to the output HTML
2. Rewrite bare filenames (`photo.jpg` → `my_post/photo.jpg`) so they resolve correctly

Remote URLs are left untouched.

---

## Build Executable (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "md2html-gui" \
  --hidden-import=pymdownx \
  --hidden-import=pymdownx.highlight \
  --hidden-import=pymdownx.superfences \
  gui.py
```

The `.exe` will be in `dist/`. Place `config.yaml` next to it for custom settings.

---

## Project Structure

```
md2html/
├── md2html.py           # Core converter (CLI)
├── gui.py               # Tkinter GUI
├── md2html-gui.exe      # Standalone Windows executable
├── config.yaml          # Default configuration
├── requirements.txt     # Python dependencies
└── .gitignore
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [markdown](https://python-markdown.github.io/) | ≥ 3.5 | Markdown parsing |
| [pymdown-extensions](https://facelessuser.github.io/pymdown-extensions/) | ≥ 10.0 | Extended Markdown features |
| [Pygments](https://pygments.org/) | ≥ 2.15 | Syntax highlighting |
| [PyYAML](https://pyyaml.org/) | ≥ 6.0 | Config file parsing |

GUI: built-in `tkinter` (ships with Python).

---

## License

MIT
