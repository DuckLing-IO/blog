#!/usr/bin/env python3
"""
Markdown to HTML converter for blog.
Converts Markdown files to self-contained, styled HTML pages.

Usage:
    python md2html.py post.md
    python md2html.py post.md -o output.html
    python md2html.py post.md -c my_config.yaml
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import markdown
import yaml

DEFAULT_CONFIG = {
    "articles_js": "",
    "site": {
        "title": "DuckLing's Blog",
        "avatar": "/img/avatar.jpg",
        "home_url": "/",
    },
    "output": {
        "default_dir": "./output"
    },
    "styles": {
        "title": {"font": "Poppins", "size": "2em", "weight": "700"},
        "heading": {"font": "Poppins"},
        "body": {"font": "Lora", "size": "16px", "line_height": "1.8"},
        "background_color": "#000000",
        "text_color": "#e0e0e0",
        "link_color": "#6ea8fe",
        "max_width": "800px",
    },
    "code": {
        "theme": "monokai",
        "show_line_numbers": False,
        "border_radius": "8px",
        "background": "#1e1e1e",
    },
    "meta": {
        "lang": "zh-CN",
        "viewport": "width=device-width, initial-scale=1.0",
    },
    "footer": {
        "text": "© 2025 - 2026 By DuckLing",
        "link_url": "https://duckee.top",
        "link_text": "DuckLing",
    },
}


def load_config(config_path: Optional[Path]) -> dict:
    """Load YAML config and deep-merge with defaults."""
    config = _deep_copy(DEFAULT_CONFIG)
    if config_path is None:
        return config

    if not config_path.exists():
        print(f"Warning: config file '{config_path}' not found, using defaults.")
        return config

    with open(config_path, "r", encoding="utf-8") as f:
        user = yaml.safe_load(f)
    if user:
        return _deep_merge(config, user)
    return config


def _deep_copy(d: dict) -> dict:
    result = {}
    for k, v in d.items():
        result[k] = _deep_copy(v) if isinstance(v, dict) else v
    return result


def _deep_merge(base: dict, override: dict) -> dict:
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            base[k] = _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def convert_md_to_html(md_text: str, config: dict) -> str:
    """Convert Markdown text to HTML body using configured extensions."""
    code_cfg = config.get("code", {})

    extension_configs = {
        "pymdownx.highlight": {
            "linenums": code_cfg.get("show_line_numbers", False),
            "auto_title": True,
            "auto_title_map": {},
            "linenums_style": "table",
            "css_class": "code-block",
        },
        "pymdownx.superfences": {},
    }

    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.toc",
            "pymdownx.highlight",
            "pymdownx.superfences",
        ],
        extension_configs=extension_configs,
    )

    return md.convert(md_text)


def generate_css(styles: dict, code_cfg: dict) -> str:
    """Build the full CSS stylesheet from config."""
    title = styles["title"]
    heading = styles.get("heading", title)
    body = styles["body"]
    bg = styles.get("background_color", "#000000")
    text = styles.get("text_color", "#e0e0e0")
    link = styles.get("link_color", "#6ea8fe")
    max_w = styles.get("max_width", "800px")
    code_bg = code_cfg.get("background", "#1e1e1e")
    radius = code_cfg.get("border_radius", "8px")

    heading_font = heading.get("font", title["font"])

    return f"""\
/* === Reset & Base === */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    background-color: {bg};
    color: {text};
    font-family: '{body["font"]}', Georgia, 'Noto Serif SC', serif;
    font-size: {body.get("size", "16px")};
    line-height: {body.get("line_height", "1.8")};
    padding: 100px 1rem 2rem;
    -webkit-font-smoothing: antialiased;
}}

/* === Site header (frosted glass) === */
.site-header {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(10,10,10,.65);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid rgba(255,255,255,.06);
}}

.site-header .header-avatar {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
}}

.site-header .header-title {{
    font-family: '{heading_font}', 'Noto Sans SC', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: #eee;
    letter-spacing: -.3px;
    text-decoration: none;
}}

.site-header .header-title:hover {{ opacity: .7; }}

.blog-post {{
    max-width: {max_w};
    margin: 0 auto;
}}

/* === Headings === */
.blog-post h1, .blog-post h2, .blog-post h3,
.blog-post h4, .blog-post h5, .blog-post h6 {{
    font-family: '{heading_font}', 'Noto Sans SC', sans-serif;
    font-weight: {title.get("weight", "700")};
    line-height: 1.3;
    margin-top: 2em;
    margin-bottom: 0.5em;
}}

.blog-post h1 {{ font-size: {title.get("size", "2em")}; }}
.blog-post h2 {{ font-size: 1.5em; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.3em; }}
.blog-post h3 {{ font-size: 1.25em; }}

/* === Post meta (date + views below title) === */
.blog-post .post-meta {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: '{heading_font}', 'Noto Sans SC', sans-serif;
    font-size: 0.875em;
    color: rgba(255,255,255,0.4);
    margin-top: 0.2em;
    margin-bottom: 2.5em;
}}

.blog-post .post-meta .post-date {{
    color: inherit;
}}

.blog-post .post-meta .post-views {{
    color: inherit;
}}

/* === Paragraph === */
.blog-post p {{ margin-bottom: 1.2em; }}

/* === Links === */
.blog-post a {{
    color: {link};
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color .2s;
}}
.blog-post a:hover {{ border-bottom-color: {link}; }}

/* === Images === */
.blog-post img {{
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 1.5em 0;
    display: block;
}}

/* === Inline code === */
.blog-post code:not(pre code) {{
    background: rgba(255,255,255,0.08);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-size: 0.9em;
    font-family: 'Cascadia Code', 'Fira Code', 'JetBrains Mono', 'Consolas', monospace;
    color: #f0c060;
}}

/* === Code block container === */
.blog-post .code-block {{
    background: {code_bg};
    border-radius: {radius}px;
    margin: 1.5em 0;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}

/* Code block header — language label (pymdownx auto_title) */
.blog-post .code-block > .filename {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5em 1em;
    background: #2d2d2d;
    color: #858585;
    font-size: 0.75em;
    font-family: '{heading_font}', 'Noto Sans SC', sans-serif;
    text-transform: uppercase;
    letter-spacing: .05em;
    user-select: none;
}}

/* Code content area */
.blog-post .code-block > pre {{
    padding: 1em;
    margin: 0;
    overflow-x: auto;
    font-family: 'Cascadia Code', 'Fira Code', 'JetBrains Mono', 'Consolas', monospace;
    font-size: 0.875em;
    line-height: 1.6;
    background: transparent;
}}

.blog-post .code-block > pre code {{
    background: transparent;
    padding: 0;
    font-size: inherit;
    color: inherit;
}}

/* Line numbers table layout */
.blog-post .code-block .linenodiv {{
    padding-right: 1em;
    border-right: 1px solid rgba(255,255,255,0.08);
    margin-right: 1em;
}}

.blog-post .code-block .linenodiv pre {{
    color: rgba(255,255,255,0.25);
    user-select: none;
}}

/* === Tables === */
.blog-post table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
}}

.blog-post th, .blog-post td {{
    border: 1px solid rgba(255,255,255,0.12);
    padding: 0.6em 0.8em;
    text-align: left;
}}

.blog-post th {{
    background: rgba(255,255,255,0.04);
    font-weight: 600;
    font-family: '{heading_font}', 'Noto Sans SC', sans-serif;
}}

/* === Blockquote === */
.blog-post blockquote {{
    border-left: 3px solid rgba(255,255,255,0.25);
    margin: 1.5em 0;
    padding: 0.5em 1em;
    color: rgba(255,255,255,0.65);
    font-style: italic;
}}

.blog-post blockquote p:last-child {{ margin-bottom: 0; }}

/* === Lists === */
.blog-post ul, .blog-post ol {{
    margin: 0.8em 0;
    padding-left: 1.5em;
}}

.blog-post li {{ margin-bottom: 0.3em; }}
.blog-post li:last-child {{ margin-bottom: 0; }}

/* === Horizontal rule === */
.blog-post hr {{
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 2.5em 0;
}}

/* === Task list === */
.blog-post .task-list-item {{
    list-style: none;
    margin-left: -1.5em;
}}

.blog-post .task-list-item input {{
    margin-right: 0.4em;
}}

/* === Footer === */
.blog-post .post-footer-sep {{
    border: none;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin: 3em 0 1.5em;
}}

.blog-post .post-footer {{
    text-align: center;
    font-family: '{heading_font}', 'Noto Sans SC', sans-serif;
    font-size: 0.8em;
    color: rgba(255,255,255,0.3);
}}

.blog-post .post-footer a {{
    color: rgba(255,255,255,0.4);
    border-bottom: none;
    transition: color .2s;
}}

.blog-post .post-footer a:hover {{
    color: {link};
}}

/* === Back link === */
.blog-post .back-link {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 3em;
    font-family: '{heading_font}', 'Noto Sans SC', sans-serif;
    font-size: 0.875em;
    color: rgba(255,255,255,0.4);
    text-decoration: none;
    border-bottom: none;
    transition: color .2s;
}}

.blog-post .back-link:hover {{
    color: #bbb;
}}
"""


_CN_WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
_EN_WEEKDAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]


def _format_post_date(now: datetime, lang: str) -> str:
    """Format a datetime like '2026-05-03 18:30 星期日'."""
    weekdays = _EN_WEEKDAYS if lang.startswith("en") else _CN_WEEKDAYS
    return f"{now:%Y-%m-%d %H:%M} {weekdays[now.weekday()]}"


def _inject_timestamp(body_html: str, now: datetime, lang: str) -> str:
    """Insert a <time> element below the first <h1>."""
    date_str = _format_post_date(now, lang)
    iso = now.isoformat(timespec="seconds")

    def _replace(m: re.Match) -> str:
        return (
            f'{m.group(0)}\n'
            f'<div class="post-meta">\n'
            f'  <time class="post-date" datetime="{iso}">{date_str}</time>\n'
            f'  <span class="post-views">· <span id="view-count">...</span> 次浏览</span>\n'
            f'</div>'
        )

    return re.sub(r"<h1[^>]*>.*?</h1>", _replace, body_html, count=1, flags=re.DOTALL)


def build_html_page(body_html: str, config: dict) -> str:
    """Wrap the converted body in a complete HTML document with styles."""
    styles = config["styles"]
    code_cfg = config["code"]
    meta = config.get("meta", {})
    site_cfg = config.get("site", {})
    footer_cfg = config.get("footer", {})
    lang = meta.get("lang", "zh-CN")

    now = datetime.now()
    body_html = _inject_timestamp(body_html, now, lang)

    # --- Site header (frosted glass) ---
    site_title = site_cfg.get("title", "")
    site_avatar = site_cfg.get("avatar", "")
    site_home = site_cfg.get("home_url", "/")
    header_html = (
        f'<header class="site-header">\n'
        f'  <img class="header-avatar" src="{site_avatar}" alt="avatar">\n'
        f'  <a class="header-title" href="{site_home}">{site_title}</a>\n'
        f'</header>'
    ) if site_title else ""

    # --- Back link ---
    back_html = f'<a class="back-link" href="{site_home}">← Home</a>'

    # --- Footer ---
    footer_html = ""
    footer_text = footer_cfg.get("text", "")
    if footer_text:
        link_url = footer_cfg.get("link_url", "")
        link_text = footer_cfg.get("link_text", "")
        if link_url and link_text and link_text in footer_text:
            footer_text = footer_text.replace(
                link_text, f'<a href="{link_url}">{link_text}</a>'
            )
        footer_html = (
            f'\n<hr class="post-footer-sep">\n'
            f'<footer class="post-footer">\n<p>{footer_text}</p>\n</footer>'
        )

    # Pygments CSS for the chosen theme
    from pygments.formatters import HtmlFormatter
    pygments_css = HtmlFormatter(style=code_cfg.get("theme", "monokai")).get_style_defs(
        ".blog-post .code-block"
    )

    # Google Fonts URL
    title_font = styles["title"]["font"]
    body_font = styles["body"]["font"]

    fonts_param = (
        f"family={title_font.replace(' ', '+')}:wght@400;600;700"
        f"&family={body_font.replace(' ', '+')}:ital,wght@0,400;0,700;1,400"
    )

    # MathJax 3 — render $...$ and $$...$$ as LaTeX math
    mathjax_block = (
        '<script>\n'
        'MathJax = {\n'
        '  tex: {\n'
        "    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],\n"
        "    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],\n"
        '    processEscapes: true\n'
        '  }\n'
        '};\n'
        '</script>\n'
        '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'
    )

    return f"""\
<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="{meta.get("viewport", "width=device-width, initial-scale=1.0")}">
<link rel="icon" href="/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts_param}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/article.css">
<style>
{pygments_css}
</style>
{mathjax_block}
</head>
<body>
{header_html}
<article class="blog-post">
{body_html}
{back_html}{footer_html}
</article>
<script src="/view-counter.js"></script>
</body>
</html>"""


def _resolve_images(body_html: str, input_md: Path, output_html: Path) -> str:
    """Copy the image folder (same stem as .md) to output and fix bare-filename img srcs."""
    stem = input_md.stem
    image_dir = input_md.parent / stem

    if not image_dir.is_dir():
        return body_html

    dest_dir = output_html.parent / stem
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(image_dir, dest_dir)

    def _fix_src(m: re.Match) -> str:
        tag = m.group(0)
        src = m.group(1)
        # Only rewrite bare filenames — paths containing / already work after copy
        if "/" not in src and "\\" not in src and (image_dir / src).is_file():
            return tag.replace(f'src="{src}"', f'src="{stem}/{src}"')
        return tag

    return re.sub(
        r'<img\s[^>]*src="([^"]+)"',
        _fix_src,
        body_html,
    )


def _append_to_articles_js(md_text: str, output_path: Path, articles_js_path: Path) -> bool:
    """Append article metadata to articles.js after successful HTML generation."""
    from datetime import date

    # Extract title from first h1 in markdown
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else output_path.stem

    # Article ID = filename without extension (post/my-post.html → my-post)
    article_id = output_path.stem

    # Date = today in YYYY-MM-DD
    date_str = date.today().isoformat()

    # Read or create articles.js
    if articles_js_path.exists():
        content = articles_js_path.read_text(encoding='utf-8')
        if f"id: '{article_id}'" in content or f'id: "{article_id}"' in content:
            print(f"  (articles.js: '{article_id}' already exists, skipped)")
            return True
    else:
        content = (
            "// ============================================================\n"
            "//  文章配置 — 在数组尾部添加新文章，页面自动按最新在前显示\n"
            "//  文章内容由 post/文章名/ 下的 HTML 文件全权渲染\n"
            "// ============================================================\n"
            "\n"
            "const articles = [\n"
            "]\n"
        )

    # Escape single quotes in title
    safe_title = title.replace("'", "\\'")

    # Insert new entry before the closing ] of the array
    new_content = re.sub(
        r'\n\]',
        f',\n  {{\n    id: \'{article_id}\',\n    title: \'{safe_title}\',\n    date: \'{date_str}\'\n  }}\n]',
        content,
        count=1,
    )

    articles_js_path.write_text(new_content, encoding='utf-8')
    print(f"  (articles.js: appended '{article_id}')")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to a styled, self-contained HTML blog post."
    )
    parser.add_argument(
        "input",
        help="Path to the Markdown file (.md) to convert",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output HTML file path (defaults to <output_dir>/<stem>.html)",
    )
    parser.add_argument(
        "-c", "--config",
        default="config.yaml",
        help="Path to YAML config file (default: config.yaml)",
    )
    parser.add_argument(
        "--articles-js",
        help="Path to articles.js for auto-append (overrides config)",
    )

    args = parser.parse_args()

    # Resolve config path — check CWD first, then script directory
    config_path = Path(args.config)
    if not config_path.exists():
        alt = Path(__file__).resolve().parent / args.config
        if alt.exists():
            config_path = alt
        else:
            print(f"Warning: '{args.config}' not found, using built-in defaults.")
            config_path = None

    config = load_config(config_path)

    # Read Markdown source
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found — {args.input}")
        sys.exit(1)

    md_text = input_path.read_text(encoding="utf-8")

    # Convert
    body_html = convert_md_to_html(md_text, config)
    full_html = build_html_page(body_html, config)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = Path(config["output"].get("default_dir", "./output"))
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{input_path.stem}.html"

    # Ensure parent directory exists (for -o paths)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    full_html = _resolve_images(full_html, input_path, output_path)

    output_path.write_text(full_html, encoding="utf-8")
    print(f"OK  {input_path}  ->  {output_path}")

    # --- Append to articles.js ---
    articles_js_path = None
    if args.articles_js:
        articles_js_path = Path(args.articles_js)
    elif config.get("articles_js"):
        articles_js_path = Path(config["articles_js"])

    if articles_js_path and not articles_js_path.is_absolute():
        articles_js_path = (Path(__file__).resolve().parent / articles_js_path).resolve()

    if articles_js_path:
        _append_to_articles_js(md_text, output_path, articles_js_path)


if __name__ == "__main__":
    main()
