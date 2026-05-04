#!/usr/bin/env python3
"""
DuckLing's Blog — GUI 管理工具
  1. 生成 HTML  — 选择 .md → post/{name}.html
  2. 修改配置    — 追加到 articles.js
  3. 本地预览    — 启动/停止 HTTP 服务
  4. 发布上线    — git add / commit / push
"""

import http.server
import os
import sys
import threading
import webbrowser
from datetime import date, datetime
from pathlib import Path
from tkinter import filedialog, messagebox

# ── Paths (resolve from exe or script location) ─────────────────
if getattr(sys, "frozen", False):
    ROOT = Path(sys.executable).resolve().parent
else:
    ROOT = Path(__file__).resolve().parent

POST_DIR = ROOT / "post"
MD2HTML_DIR = ROOT / "md2html"
CONFIG_PATH = MD2HTML_DIR / "config.yaml"
ARTICLES_JS = ROOT / "articles.js"

from blog_core import (
    step1_generate,
    step2_update_config,
    step3_create_server,
    step4_publish,
    build_commit_message,
)

# ── Dark theme colours ────────────────────────────────────────
BG = "#111111"
FG = "#cccccc"
ACCENT = "#3a7bd5"
BTN_BG = "#1e1e1e"
BTN_FG = "#dddddd"
LOG_BG = "#0a0a0a"

# ── Helpers ───────────────────────────────────────────────────
def _extract_title(md_path: Path) -> str:
    import re
    try:
        text = md_path.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        return m.group(1).strip() if m else md_path.stem
    except Exception:
        return md_path.stem


class App:
    def __init__(self):
        import tkinter as tk
        self._tk = tk
        self.root = tk.Tk()
        self.root.title("DuckLing's Blog Manager")
        self.root.geometry("540x520")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # State
        self._last_md: Path | None = None
        self._last_output: Path | None = None
        self._server = None
        self._daily_count = 0
        self._today = date.today()

        self._build_ui()

    def run(self):
        self.root.mainloop()

    # ── UI ─────────────────────────────────────────────────────
    def _build_ui(self):
        tk = self._tk

        tk.Label(
            self.root, text="DuckLing's Blog",
            font=("Segoe UI", 18, "bold"), fg="#ffffff", bg=BG,
        ).pack(pady=(24, 18))

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack()

        self._mk_btn(btn_frame, "1. 生成 HTML",  self._do_generate)
        self._mk_btn(btn_frame, "2. 修改配置",   self._do_update_config)
        self._mk_btn(btn_frame, "3. 本地预览",   self._do_preview)
        self._mk_btn(btn_frame, "4. 发布上线",   self._do_publish)

        tk.Label(
            self.root, text="输出日志", font=("Segoe UI", 10), fg="#555", bg=BG,
        ).pack(anchor="w", padx=40, pady=(18, 4))

        self.log = tk.Text(
            self.root, height=8, bg=LOG_BG, fg=FG,
            font=("Consolas", 10), bd=0, padx=12, pady=10,
            insertbackground=FG, state="disabled",
            highlightthickness=1, highlightbackground="#222",
        )
        self.log.pack(fill="x", padx=40, pady=(0, 20))

    def _mk_btn(self, parent, text, cmd):
        tk = self._tk
        btn = tk.Button(
            parent, text=text,
            font=("Segoe UI", 12), fg=BTN_FG, bg=BTN_BG,
            activeforeground="#fff", activebackground="#2a2a2a",
            bd=0, padx=28, pady=10, cursor="hand2",
            highlightthickness=1, highlightbackground="#333",
            command=cmd,
        )
        btn.pack(fill="x", pady=5)

    # ── Log ────────────────────────────────────────────────────
    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    # ── 1. Generate HTML ───────────────────────────────────────
    def _do_generate(self):
        md_path = filedialog.askopenfilename(
            title="选择 Markdown 文件",
            filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
            initialdir=ROOT / "markdown",
        )
        if not md_path:
            return

        md_path = Path(md_path)
        title = _extract_title(md_path)
        self._log(f"生成: {md_path.name}  →  post/{md_path.stem}.html")

        ok, msg = step1_generate(md_path, POST_DIR, MD2HTML_DIR, CONFIG_PATH)
        self._log(msg)

        if ok:
            self._last_md = md_path
            self._last_output = POST_DIR / f"{md_path.stem}.html"
            # Daily counter
            today = date.today()
            if today != self._today:
                self._today = today
                self._daily_count = 0
            self._daily_count += 1
            self._log(f"✓ 文章「{title}」已生成")
        else:
            self._last_md = None
            self._last_output = None

    # ── 2. Update config ───────────────────────────────────────
    def _do_update_config(self):
        if not self._last_md or not self._last_output:
            # Fallback: let user select a file
            md_path = filedialog.askopenfilename(
                title="选择 Markdown 文件",
                filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
                initialdir=ROOT / "markdown",
            )
            if not md_path:
                return
            md_path = Path(md_path)
            output_path = POST_DIR / f"{md_path.stem}.html"
        else:
            md_path = self._last_md
            output_path = self._last_output

        self._log(f"修改配置: {md_path.stem}")
        ok, msg = step2_update_config(md_path, output_path, ARTICLES_JS)
        self._log(msg)

    # ── 3. Preview ─────────────────────────────────────────────
    def _do_preview(self):
        if self._server is not None:
            self._log("停止预览服务")
            self._stop_server()
            return

        self._log("启动预览服务 → http://127.0.0.1:8080")

        server, err = step3_create_server(ROOT, 8080)
        if server is None:
            self._log(f"✗ {err}")
            return

        self._server = server

        def _serve():
            try:
                self._server.serve_forever()
            except Exception:
                pass  # server was shut down

        t = threading.Thread(target=_serve, daemon=True)
        t.start()

        self._log("服务已启动 → http://127.0.0.1:8080")
        webbrowser.open("http://127.0.0.1:8080")

    def _stop_server(self):
        if self._server is None:
            return
        try:
            self._server.shutdown()
        except Exception:
            pass
        self._server = None
        self._log("预览服务已停止")

    # ── 4. Publish ─────────────────────────────────────────────
    def _do_publish(self):
        tk = self._tk
        default_msg = build_commit_message(self._daily_count)

        dlg = tk.Toplevel(self.root)
        dlg.title("提交信息")
        dlg.geometry("420x150")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.transient(self.root)
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
            self._run_publish(msg)

        tk.Button(
            dlg, text="确认提交", font=("Segoe UI", 11),
            fg=BTN_FG, bg=ACCENT, bd=0, padx=24, pady=6,
            activeforeground="#fff", activebackground="#4a8be5",
            command=_do,
        ).pack(pady=16)

    def _run_publish(self, msg):
        self._log(f"git push: {msg}")
        ok, output = step4_publish(ROOT, msg)
        self._log(output)


if __name__ == "__main__":
    app = App()
    app.run()
