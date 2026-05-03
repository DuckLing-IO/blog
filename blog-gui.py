#!/usr/bin/env python3
"""
DuckLing's Blog — 管理工具
  1. 选择 .md 文件 → 自动生成 HTML 到 /post/ 下
  2. 启动本地预览服务 → 浏览器打开
  3. 一键 git add / commit / push
"""

import http.server
import os
import re
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parent
POST_DIR = ROOT / "post"
MD2HTML = ROOT / "md2html" / "md2html.py"
CONFIG = ROOT / "md2html" / "config.yaml"
ARTICLES_JS = ROOT / "articles.js"

# ── Dark theme colours ────────────────────────────────────────
BG = "#111111"
FG = "#cccccc"
ACCENT = "#3a7bd5"
BTN_BG = "#1e1e1e"
BTN_FG = "#dddddd"
LOG_BG = "#0a0a0a"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DuckLing's Blog Manager")
        self.geometry("520x460")
        self.configure(bg=BG)
        self.resizable(False, False)

        self._last_title = ""   # title extracted from the last generated article
        self._server = None

        self._build_ui()

    # ── UI ─────────────────────────────────────────────────────
    def _build_ui(self):
        # Title
        tk.Label(
            self, text="DuckLing's Blog",
            font=("Segoe UI", 18, "bold"), fg="#ffffff", bg=BG,
        ).pack(pady=(24, 18))

        # Buttons frame
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack()

        self._mk_btn(btn_frame, "📄  生成 HTML", self._generate, 0)
        self._mk_btn(btn_frame, "🌐  启动预览",  self._preview,  1)
        self._mk_btn(btn_frame, "🚀  上传 GitHub", self._push,    2)

        # Log area
        tk.Label(
            self, text="输出日志", font=("Segoe UI", 10), fg="#555", bg=BG,
        ).pack(anchor="w", padx=40, pady=(18, 4))

        self.log = tk.Text(
            self, height=8, bg=LOG_BG, fg=FG,
            font=("Consolas", 10), bd=0, padx=12, pady=10,
            insertbackground=FG, state="disabled",
            highlightthickness=1, highlightbackground="#222",
        )
        self.log.pack(fill="x", padx=40, pady=(0, 20))

    def _mk_btn(self, parent, text, cmd, row):
        """Styled button."""
        btn = tk.Button(
            parent, text=text,
            font=("Segoe UI", 12), fg=BTN_FG, bg=BTN_BG,
            activeforeground="#fff", activebackground="#2a2a2a",
            bd=0, padx=28, pady=10, cursor="hand2",
            highlightthickness=1, highlightbackground="#333",
            command=cmd,
        )
        btn.pack(fill="x", pady=5)

    # ── Log helper ─────────────────────────────────────────────
    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
        self.update()

    # ── 1. Generate HTML ───────────────────────────────────────
    def _generate(self):
        md_path = filedialog.askopenfilename(
            title="选择 Markdown 文件",
            filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
            initialdir=ROOT / "markdown",
        )
        if not md_path:
            return

        md_path = Path(md_path)

        # Extract title from markdown
        title = self._extract_title(md_path)
        self._last_title = title

        # Article id = stem (folder name under post/)
        article_id = md_path.stem

        # Output path
        output_path = POST_DIR / article_id / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        self._log(f"生成: {md_path.name}  →  post/{article_id}/index.html")

        try:
            r = subprocess.run(
                [
                    sys.executable, str(MD2HTML),
                    str(md_path),
                    "-c", str(CONFIG),
                    "-o", str(output_path),
                ],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            self._log(r.stdout.strip())
            if r.stderr.strip():
                self._log(r.stderr.strip())

            if r.returncode == 0:
                self._log(f"✓ 完成 — 文章「{title}」已生成")
            else:
                self._log("✗ 转换失败，请检查上方错误信息")
        except Exception as e:
            self._log(f"✗ 错误: {e}")

    # ── 2. Preview ─────────────────────────────────────────────
    def _preview(self):
        if self._server:
            self._log("预览服务已在运行 → http://localhost:8080")
            webbrowser.open("http://localhost:8080")
            return

        self._log("启动预览服务 → http://localhost:8080")

        def _serve():
            try:
                handler = http.server.SimpleHTTPRequestHandler
                self._server = http.server.HTTPServer(
                    ("0.0.0.0", 8080), handler, bind_and_activate=True
                )
                self._server.directory = str(ROOT)
            except OSError:
                self._log("✗ 端口 8080 被占用，请先关闭占用进程")
                self._server = None
                return

            webbrowser.open("http://localhost:8080")
            self._server.serve_forever()

        t = threading.Thread(target=_serve, daemon=True)
        t.start()

    # ── 3. Push ────────────────────────────────────────────────
    def _push(self):
        now = datetime.now()
        default_msg = (
            f"{now:%Y-%m-%d %H:%M}"
            + (f" — {self._last_title}" if self._last_title else "")
        )

        # Simple input dialog
        dlg = tk.Toplevel(self)
        dlg.title("提交信息")
        dlg.geometry("420x150")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()

        tk.Label(
            dlg, text="Commit message", font=("Segoe UI", 11),
            fg=FG, bg=BG,
        ).pack(pady=(16, 4))

        entry = tk.Entry(
            dlg, font=("Consolas", 11), bg=LOG_BG, fg=FG,
            insertbackground=FG, bd=0, relief="flat",
            highlightthickness=1, highlightbackground="#333",
        )
        entry.insert(0, default_msg)
        entry.pack(fill="x", padx=20, ipady=4)
        entry.select_range(0, "end")
        entry.focus()

        def _do():
            msg = entry.get().strip()
            if not msg:
                messagebox.showwarning("警告", "请输入 commit message")
                return
            dlg.destroy()
            self._run_push(msg)

        tk.Button(
            dlg, text="确认提交", font=("Segoe UI", 11),
            fg=BTN_FG, bg=ACCENT, bd=0, padx=24, pady=6,
            activeforeground="#fff", activebackground="#4a8be5",
            command=_do,
        ).pack(pady=16)

    def _run_push(self, msg):
        self._log(f"git add -A")
        self._log(f'git commit -m "{msg}"')
        self._log("git push")

        try:
            cmds = [
                ["git", "add", "-A"],
                ["git", "commit", "-m", msg],
                ["git", "push"],
            ]
            for cmd in cmds:
                r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
                if r.stdout.strip():
                    self._log(r.stdout.strip())
                if r.stderr.strip():
                    self._log(r.stderr.strip())
                if r.returncode != 0:
                    self._log(f"✗ {' '.join(cmd)} 失败")
                    return
                self.update()
            self._log("✓ 推送成功")
        except Exception as e:
            self._log(f"✗ 错误: {e}")

    # ── Helpers ────────────────────────────────────────────────
    @staticmethod
    def _extract_title(md_path: Path) -> str:
        """Extract first # heading from markdown."""
        try:
            text = md_path.read_text(encoding="utf-8")
            m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            return m.group(1).strip() if m else md_path.stem
        except Exception:
            return md_path.stem


if __name__ == "__main__":
    app = App()
    app.mainloop()
