#!/usr/bin/env python3
"""
md2html GUI — 图形化 Markdown → HTML 转换工具。
基于 tkinter，内置中文错误提示。
"""

import sys
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
import threading

from md2html import (
    load_config,
    convert_md_to_html,
    build_html_page,
    _resolve_images,
)

FONT = ("Microsoft YaHei UI", 10)
FONT_BOLD = ("Microsoft YaHei UI", 10, "bold")


def _get_config_path():
    """Locate config.yaml next to the script/exe, return None if missing."""
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).resolve().parent
    cfg = base / "config.yaml"
    return cfg if cfg.exists() else None


def _wrap_convert(app: "App") -> None:
    """Run conversion in a background thread to keep UI responsive."""
    app.btn_convert.config(state="disabled", text="转换中...")
    app.log("开始转换...")

    try:
        # --- Validate input ---
        raw_input = app.input_var.get().strip()
        if not raw_input:
            app.log("错误: 请输入 Markdown 文件路径，或点击 [浏览...] 选择文件。")
            app._reset_button()
            return

        input_path = Path(raw_input).resolve()
        app.log(f"输入文件: {input_path}")

        if not input_path.exists():
            app.log("错误: 输入文件不存在，请检查路径。")
            app._reset_button()
            return
        if input_path.suffix.lower() not in (".md", ".markdown", ".mdown", ".mkd"):
            app.log("错误: 输入文件不是 Markdown 文件（.md / .markdown）。")
            app._reset_button()
            return

        # --- Config: always look next to the script/exe ---
        config_path = _get_config_path()
        config = load_config(config_path)
        app.log(f"已加载配置" + (f" ({config_path})" if config_path else "（内置默认值）"))

        # --- Resolve output path (always absolute) ---
        out_str = app.output_var.get().strip()
        if out_str:
            output_path = Path(out_str).resolve()
        else:
            output_path = None

        if output_path is None:
            out_dir = Path(config.get("output", {}).get("default_dir", "./output")).resolve()
            out_dir.mkdir(parents=True, exist_ok=True)
            output_path = (out_dir / f"{input_path.stem}.html").resolve()
        else:
            output_path = output_path.resolve()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        app.log(f"输出目标: {output_path}")

        # --- Read & convert ---
        md_text = input_path.read_text(encoding="utf-8")
        body_html = convert_md_to_html(md_text, config)
        full_html = build_html_page(body_html, config)

        # --- Handle local images ---
        full_html = _resolve_images(full_html, input_path, output_path)

        # --- Write ---
        output_path.write_text(full_html, encoding="utf-8")

        # Verify the file was actually written
        if output_path.exists() and output_path.stat().st_size > 0:
            app.log(f"转换成功! 已生成: {output_path}")
        else:
            app.log(f"严重错误: 文件写入后验证失败，请检查磁盘空间和目录权限。")

    except PermissionError:
        app.log(f"错误: 没有写入权限，请检查目标目录 ({output_path.parent}) 是否可写。")
    except Exception as exc:
        app.log(f"转换失败: {exc}")

    finally:
        app._reset_button()


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("MD → HTML 转换器")
        root.resizable(True, True)
        root.minsize(560, 380)

        # --- Variables ---
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()

        # --- Build UI ---
        self._build()
        cfg = _get_config_path()
        if cfg:
            self.log(f"配置文件: {cfg}")
        else:
            self.log("未找到 config.yaml，将使用内置默认值。")
        self.log("就绪 — 请选择要转换的 Markdown 文件。")

    def _build(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        # --- Row 1: input file ---
        ttk.Label(frame, text="输入文件 (.md):", font=FONT_BOLD).grid(
            row=0, column=0, sticky="w", pady=(0, 2)
        )
        input_row = ttk.Frame(frame)
        input_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        ttk.Entry(input_row, textvariable=self.input_var, font=FONT).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(input_row, text="浏览...", command=self._select_input).pack(
            side="right", padx=(6, 0)
        )

        # --- Row 2: output file ---
        ttk.Label(frame, text="输出文件 (.html):", font=FONT_BOLD).grid(
            row=2, column=0, sticky="w", pady=(0, 2)
        )
        output_row = ttk.Frame(frame)
        output_row.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        ttk.Entry(output_row, textvariable=self.output_var, font=FONT).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(output_row, text="浏览...", command=self._select_output).pack(
            side="right", padx=(6, 0)
        )

        # --- Convert button ---
        self.btn_convert = ttk.Button(
            frame, text="开始转换", command=self._on_convert
        )
        self.btn_convert.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # --- Log area ---
        ttk.Label(frame, text="运行日志:", font=FONT_BOLD).grid(
            row=5, column=0, sticky="w", pady=(0, 2)
        )
        self.log_text = tk.Text(
            frame,
            height=10,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            relief="flat",
            borderwidth=2,
            wrap="word",
        )
        self.log_text.grid(row=6, column=0, columnspan=2, sticky="nsew")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=6, column=2, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Grid weights
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(6, weight=1)

    # --- File dialogs ---

    def _select_input(self):
        path = filedialog.askopenfilename(
            title="选择 Markdown 文件",
            filetypes=[("Markdown 文件", "*.md *.markdown *.mdown *.mkd"), ("所有文件", "*.*")],
        )
        if path:
            p = Path(path).resolve()
            self.input_var.set(str(p))
            self.output_var.set(str(p.parent / "output" / f"{p.stem}.html"))

    def _select_output(self):
        path = filedialog.asksaveasfilename(
            title="保存 HTML 文件",
            defaultextension=".html",
            filetypes=[("HTML 文件", "*.html"), ("所有文件", "*.*")],
        )
        if path:
            self.output_var.set(path)

    def _on_convert(self):
        threading.Thread(target=_wrap_convert, args=(self,), daemon=True).start()

    def _reset_button(self):
        self.btn_convert.after(0, lambda: self.btn_convert.config(
            state="normal", text="开始转换"
        ))

    def log(self, msg: str):
        """Thread-safe log append."""
        self.log_text.after(0, lambda: self._append(msg))

    def _append(self, msg: str):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
