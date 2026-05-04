"""
Blog workflow — four independent steps.
Each function returns (ok: bool, message: str).
"""

import http.server
import os
import re
import shutil
import socket
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional


# ── Shared article CSS ────────────────────────────────────────────
def generate_article_css(
    project_root: Path,
    md2html_dir: Path,
    config_path: Path,
) -> bool:
    """Generate /article.css from config.yaml.  Returns True on success."""
    try:
        sys.path.insert(0, str(md2html_dir))
        import md2html as m2h
        from pygments.formatters import HtmlFormatter

        config = m2h.load_config(config_path)
        css = m2h.generate_css(config["styles"], config["code"])
        pygments_css = HtmlFormatter(
            style=config["code"].get("theme", "monokai")
        ).get_style_defs(".blog-post .code-block")

        out = project_root / "article.css"
        out.write_text(
            "/* Shared article styles — generated from config.yaml */\n\n"
            + css
            + "\n\n/* === Pygments code highlighting === */\n"
            + pygments_css
            + "\n",
            encoding="utf-8",
        )
        return True
    except Exception:
        return False


# ── Step 1: Generate HTML from Markdown ──────────────────────────
def step1_generate(
    md_path: Path,
    post_dir: Path,
    md2html_dir: Path,
    config_path: Path,
    article_datetime: Optional[str] = None,
) -> tuple:
    """Convert .md → post/{name}.html and copy images to post/{name}/.

    If article_datetime is given (YYYY-MM-DD HH:MM), it replaces the
    auto-generated timestamp in the HTML.
    """
    if not md_path.exists():
        return False, f"文件不存在: {md_path}"

    article_id = md_path.stem
    output_path = post_dir / f"{article_id}.html"
    post_dir.mkdir(parents=True, exist_ok=True)

    # Ensure shared article.css is up to date
    project_root = post_dir.parent
    generate_article_css(project_root, md2html_dir, config_path)

    try:
        sys.path.insert(0, str(md2html_dir))
        import md2html as m2h

        config = m2h.load_config(config_path)
        md_text = md_path.read_text(encoding="utf-8")
        body_html = m2h.convert_md_to_html(md_text, config)
        full_html = m2h.build_html_page(body_html, config)
        full_html = m2h._resolve_images(full_html, md_path, output_path)

        # Replace auto-generated timestamp with user-specified datetime
        if article_datetime:
            full_html = re.sub(
                r'<time class="post-date" datetime="[^"]*">[^<]*</time>',
                f'<time class="post-date" datetime="{article_datetime}">{article_datetime}</time>',
                full_html,
            )

        output_path.write_text(full_html, encoding="utf-8")

        return True, f"OK  {md_path.name}  →  post/{article_id}.html"
    except Exception as e:
        return False, f"生成失败: {e}"


# ── Step 2: Update articles.js config ────────────────────────────
def step2_update_config(
    md_path: Path,
    output_path: Path,
    articles_js_path: Path,
    article_datetime: Optional[str] = None,
) -> tuple:
    """Append article metadata to articles.js."""
    if not md_path.exists():
        return False, f"文件不存在: {md_path}"

    try:
        md_text = md_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"读取失败: {e}"

    # Extract title from first h1
    m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    title = m.group(1).strip() if m else md_path.stem

    article_id = output_path.stem
    date_str = article_datetime or datetime.now().strftime("%Y-%m-%d %H:%M")

    # Read or create articles.js
    if articles_js_path.exists():
        content = articles_js_path.read_text(encoding="utf-8")
        if f"id: '{article_id}'" in content or f'id: "{article_id}"' in content:
            return True, f"articles.js: '{article_id}' 已存在，跳过"
    else:
        content = (
            "// ============================================================\n"
            "//  文章配置 — 在数组尾部添加新文章，页面自动按最新在前显示\n"
            "//  文章内容由 post/ 下的 HTML 文件全权渲染\n"
            "// ============================================================\n"
            "\n"
            "const articles = [\n"
            "]\n"
        )

    safe_title = title.replace("'", "\\'")

    new_content = re.sub(
        r"\n\]",
        f",\n  {{\n    id: '{article_id}',\n    title: '{safe_title}',\n    date: '{date_str}'\n  }}\n]",
        content,
        count=1,
    )

    try:
        articles_js_path.write_text(new_content, encoding="utf-8")
        return True, f"articles.js: 已添加「{title}」"
    except Exception as e:
        return False, f"写入 articles.js 失败: {e}"


# ── Step 3: Preview server ───────────────────────────────────────
def step3_create_server(root_dir: Path, port: int = 8080):
    """Create an HTTP server bound to 127.0.0.1:port serving root_dir.

    Returns (server, None) on success, or (None, error_msg) on failure.
    """
    import posixpath
    from urllib.parse import unquote

    root_str = str(root_dir.resolve())

    class _Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            """Serve files from root_dir, prevent path traversal."""
            path = posixpath.normpath(unquote(path))
            words = path.split("/")
            words = (w for w in words if w)
            result = root_str
            for word in words:
                if os.pardir in word:
                    continue
                result = os.path.join(result, word)
            return result

        def log_message(self, format, *args):
            pass  # suppress request logs to stderr

    try:
        server = http.server.HTTPServer(("127.0.0.1", port), _Handler)
        server.allow_reuse_address = True
        return server, None
    except OSError as e:
        return None, f"端口 {port} 被占用: {e}"


# ── Step 4: Git publish ──────────────────────────────────────────
def step4_publish(root_dir: Path, commit_msg: str) -> tuple:
    """Run git add -A, git commit, git push. Returns (ok, message)."""
    lines = []

    def _run(cmd, label):
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True,
                cwd=str(root_dir), timeout=60,
            )
        except subprocess.TimeoutExpired:
            lines.append(f"✗ {label} 超时（60s）")
            return None
        except Exception as e:
            lines.append(f"✗ {label} 异常: {e}")
            return None
        out = r.stdout.strip()
        err = r.stderr.strip()
        if out:
            lines.append(out)
        if err:
            lines.append(err)
        if r.returncode != 0:
            lines.append(f"✗ {label} 失败 (exit {r.returncode})")
            return None
        return r

    # git add
    if _run(["git", "add", "-A"], "git add") is None:
        return False, "\n".join(lines)

    # git commit
    if _run(["git", "commit", "-m", commit_msg], "git commit") is None:
        return False, "\n".join(lines)

    # Determine push command (check upstream silently)
    r_upstream = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "@{upstream}"],
        capture_output=True, text=True,
        cwd=str(root_dir), timeout=10,
    )
    if r_upstream.returncode == 0:
        push_cmd = ["git", "push"]
    else:
        r_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True,
            cwd=str(root_dir), timeout=10,
        )
        branch = r_branch.stdout.strip()
        lines.append(f"分支 '{branch}' 无上游，自动设置 origin/{branch}")
        push_cmd = ["git", "push", "-u", "origin", branch]

    if _run(push_cmd, "git push") is None:
        return False, "\n".join(lines)

    lines.append("✓ 推送成功")
    return True, "\n".join(lines)


# ── Step 5: Delete article ────────────────────────────────────────
def step5_delete_article(
    article_id: str,
    post_dir: Path,
    articles_js_path: Path,
) -> tuple:
    """Delete HTML file, image folder, and articles.js entry for an article."""
    html_path = post_dir / f"{article_id}.html"
    img_dir = post_dir / article_id

    deleted = []

    # Delete HTML file
    if html_path.exists():
        html_path.unlink()
        deleted.append(f"post/{article_id}.html")
    else:
        return False, f"文件不存在: post/{article_id}.html"

    # Delete image folder
    if img_dir.is_dir():
        shutil.rmtree(img_dir)
        deleted.append(f"post/{article_id}/")

    # Remove from articles.js
    if articles_js_path.exists():
        content = articles_js_path.read_text(encoding="utf-8")
        # Remove the entry block: { id: 'xxx', title: '...', date: '...' }
        pattern = re.compile(
            r",?\s*\{\s*\n?\s*id:\s*['\"]" + re.escape(article_id) + r"['\"].*?\n\s*\}",
            re.DOTALL,
        )
        new_content = pattern.sub("", content, count=1)
        if new_content != content:
            articles_js_path.write_text(new_content, encoding="utf-8")
            deleted.append("articles.js 条目")

    return True, f"已删除: {', '.join(deleted)}"


# ── Commit message helper ────────────────────────────────────────
def build_commit_message(daily_count: int) -> str:
    """Return commit message in yy-mm-dd_x format."""
    now = datetime.now()
    n = daily_count if daily_count > 0 else 1
    return f"{now:%y-%m-%d}_{n}"
