#!/usr/bin/env python3
"""DuckLing Blog Studio - desktop article manager for the Jekyll blog."""

from __future__ import annotations

import io
import ctypes
import os
import shutil
import subprocess
import sys
import threading
import traceback
import webbrowser
from contextlib import redirect_stdout
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import (
    BOTH,
    END,
    HORIZONTAL,
    LEFT,
    RIGHT,
    X,
    Y,
    BooleanVar,
    StringVar,
    Tk,
    filedialog,
    messagebox,
    simpledialog,
    ttk,
)
import tkinter as tk
from urllib.parse import quote

import blog


APP_NAME = "DuckLing Blog Studio"
SITE_URL = "https://blog.duckee.top"

INK = "#0B1112"
PANEL = "#11191A"
PANEL_RAISED = "#162021"
RULE = "#283533"
PAPER = "#E9EFEA"
MUTED = "#819088"
DUCK_EGG = "#9FC5B0"
DUCK_EGG_DARK = "#6E9B83"
DANGER = "#D7877F"
WARNING = "#D6B574"

UI_FONT = "Microsoft YaHei UI"
DISPLAY_FONT = "Segoe UI Variable Display"
MONO_FONT = "Cascadia Code"


@dataclass
class Article:
    path: Path
    metadata: dict
    body: str
    state: str
    title: str
    date: str
    slug: str


def hidden_startupinfo() -> subprocess.STARTUPINFO | None:
    if os.name != "nt":
        return None
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return info


class BlogStudio(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.minsize(1040, 680)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = min(1280, max(1040, screen_width - 80))
        window_height = min(790, max(680, screen_height - 100))
        offset_x = max(0, (screen_width - window_width) // 2)
        offset_y = max(0, (screen_height - window_height) // 2)
        self.geometry(f"{window_width}x{window_height}+{offset_x}+{offset_y}")
        self.configure(bg=INK)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.articles: list[Article] = []
        self.article_by_iid: dict[str, Article] = {}
        self.current: Article | None = None
        self.current_path: Path | None = None
        self.current_metadata: dict = {}
        self.dirty = False
        self.loading = False
        self.git_busy = False

        self.search_var = StringVar()
        self.filter_var = StringVar(value="all")
        self.title_var = StringVar()
        self.date_var = StringVar()
        self.slug_var = StringVar()
        self.article_state_var = StringVar(value="draft")
        self.stats_var = StringVar(value="正在读取文章…")
        self.footer_status_var = StringVar(value=f"项目 · {blog.ROOT}")

        self._configure_style()
        self._build_ui()
        self._bind_events()
        self.reload_articles(select_first=True)

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=INK, foreground=PAPER, font=(UI_FONT, 10))
        style.configure("App.TFrame", background=INK)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Raised.TFrame", background=PANEL_RAISED)
        style.configure("Brand.TLabel", background=PANEL, foreground=PAPER,
                        font=(DISPLAY_FONT, 21, "bold"))
        style.configure("Eyebrow.TLabel", background=PANEL, foreground=DUCK_EGG,
                        font=(MONO_FONT, 9, "bold"))
        style.configure("Stats.TLabel", background=PANEL, foreground=MUTED,
                        font=(UI_FONT, 9))
        style.configure("EditorTitle.TLabel", background=INK, foreground=PAPER,
                        font=(DISPLAY_FONT, 24, "bold"))
        style.configure("Field.TLabel", background=INK, foreground=MUTED,
                        font=(UI_FONT, 9))
        style.configure("Hint.TLabel", background=INK, foreground=MUTED,
                        font=(UI_FONT, 9))
        style.configure("Footer.TLabel", background=PANEL, foreground=MUTED,
                        font=(MONO_FONT, 8))

        style.configure("TEntry", fieldbackground=PANEL_RAISED, foreground=PAPER,
                        insertcolor=PAPER, bordercolor=RULE, lightcolor=RULE,
                        darkcolor=RULE, padding=(10, 8))
        style.map("TEntry", bordercolor=[("focus", DUCK_EGG)])

        style.configure("Primary.TButton", background=DUCK_EGG, foreground=INK,
                        borderwidth=0, padding=(16, 9), font=(UI_FONT, 10, "bold"))
        style.map("Primary.TButton", background=[("active", "#B5D4C2"), ("disabled", RULE)])
        style.configure("Secondary.TButton", background=PANEL_RAISED, foreground=PAPER,
                        bordercolor=RULE, padding=(13, 8))
        style.map("Secondary.TButton", background=[("active", RULE)])
        style.configure("Danger.TButton", background=PANEL_RAISED, foreground=DANGER,
                        bordercolor=RULE, padding=(13, 8))
        style.map("Danger.TButton", background=[("active", "#2A2020")])
        style.configure("Filter.TRadiobutton", background=PANEL, foreground=MUTED,
                        indicatorcolor=PANEL, indicatormargin=0, padding=(10, 6))
        style.map("Filter.TRadiobutton",
                  background=[("selected", RULE), ("active", PANEL_RAISED)],
                  foreground=[("selected", PAPER), ("active", PAPER)],
                  indicatorcolor=[("selected", DUCK_EGG)])

        style.configure("Articles.Treeview", background=PANEL, fieldbackground=PANEL,
                        foreground=PAPER, borderwidth=0, rowheight=51,
                        font=(UI_FONT, 10))
        style.configure("Articles.Treeview.Heading", background=PANEL, foreground=MUTED,
                        borderwidth=0, font=(MONO_FONT, 8, "bold"), padding=(5, 8))
        style.map("Articles.Treeview", background=[("selected", "#263530")],
                  foreground=[("selected", PAPER)])
        style.configure("TScrollbar", background=RULE, troughcolor=PANEL,
                        bordercolor=PANEL, arrowcolor=MUTED)
        style.configure("Sync.Horizontal.TProgressbar", troughcolor=PANEL_RAISED,
                        background=DUCK_EGG, bordercolor=PANEL_RAISED, lightcolor=DUCK_EGG,
                        darkcolor=DUCK_EGG)

    def _build_ui(self) -> None:
        shell = ttk.Frame(self, style="App.TFrame")
        shell.pack(fill=BOTH, expand=True)

        self.sidebar = ttk.Frame(shell, style="Panel.TFrame", width=390)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)
        self.editor = ttk.Frame(shell, style="App.TFrame")
        self.editor.pack(side=LEFT, fill=BOTH, expand=True)

        # The mint ledger spine is the visual anchor for the article archive.
        spine = tk.Frame(self.sidebar, bg=DUCK_EGG, width=4)
        spine.pack(side=LEFT, fill=Y)
        side_content = ttk.Frame(self.sidebar, style="Panel.TFrame")
        side_content.pack(side=LEFT, fill=BOTH, expand=True, padx=(22, 18), pady=(24, 14))

        ttk.Label(side_content, text="DUCKLING · LEDGER", style="Eyebrow.TLabel").pack(anchor="w")
        ttk.Label(side_content, text="文章编辑台", style="Brand.TLabel").pack(anchor="w", pady=(3, 2))
        ttk.Label(side_content, textvariable=self.stats_var, style="Stats.TLabel").pack(anchor="w")

        controls = ttk.Frame(side_content, style="Panel.TFrame")
        controls.pack(fill=X, pady=(20, 11))
        ttk.Button(controls, text="＋ 新建草稿", style="Primary.TButton",
                   command=self.new_draft).pack(side=LEFT)
        ttk.Button(controls, text="导入 Markdown", style="Secondary.TButton",
                   command=self.import_markdown).pack(side=LEFT, padx=(8, 0))

        search_box = ttk.Entry(side_content, textvariable=self.search_var)
        search_box.pack(fill=X, pady=(0, 10))
        search_box.insert(0, "")

        filters = ttk.Frame(side_content, style="Panel.TFrame")
        filters.pack(fill=X, pady=(0, 8))
        for text, value in (("全部", "all"), ("已发布", "published"), ("草稿", "draft")):
            ttk.Radiobutton(filters, text=text, value=value, variable=self.filter_var,
                            style="Filter.TRadiobutton").pack(side=LEFT, padx=(0, 5))

        list_wrap = ttk.Frame(side_content, style="Panel.TFrame")
        list_wrap.pack(fill=BOTH, expand=True)
        self.article_tree = ttk.Treeview(
            list_wrap,
            columns=("state", "date"),
            show="tree headings",
            style="Articles.Treeview",
            selectmode="browse",
        )
        self.article_tree.heading("#0", text="文章")
        self.article_tree.heading("state", text="状态")
        self.article_tree.heading("date", text="日期")
        self.article_tree.column("#0", width=184, minwidth=130, stretch=True)
        self.article_tree.column("state", width=55, minwidth=55, stretch=False, anchor="center")
        self.article_tree.column("date", width=76, minwidth=76, stretch=False, anchor="e")
        self.article_tree.tag_configure("draft", foreground=WARNING)
        self.article_tree.tag_configure("published", foreground=PAPER)
        scrollbar = ttk.Scrollbar(list_wrap, orient="vertical", command=self.article_tree.yview)
        self.article_tree.configure(yscrollcommand=scrollbar.set)
        self.article_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self._build_footer()
        self._build_editor()

    def _build_editor(self) -> None:
        content = ttk.Frame(self.editor, style="App.TFrame")
        content.pack(fill=BOTH, expand=True, padx=34, pady=(26, 14))

        top = ttk.Frame(content, style="App.TFrame")
        top.pack(fill=X)
        heading = ttk.Frame(top, style="App.TFrame")
        heading.pack(side=LEFT, fill=X, expand=True)
        ttk.Label(heading, text="MARKDOWN / LIVE SOURCE", style="Field.TLabel").pack(anchor="w")
        ttk.Label(heading, text="正文工作区", style="EditorTitle.TLabel").pack(anchor="w", pady=(2, 0))

        self.state_chip = tk.Label(
            top,
            text="草稿",
            bg=WARNING,
            fg=INK,
            font=(UI_FONT, 9, "bold"),
            padx=12,
            pady=6,
        )
        self.state_chip.pack(side=RIGHT, anchor="n", pady=(7, 0))

        form = ttk.Frame(content, style="App.TFrame")
        form.pack(fill=X, pady=(20, 14))
        form.columnconfigure(0, weight=5)
        form.columnconfigure(1, weight=3)
        form.columnconfigure(2, weight=4)

        self._field(form, "文章标题", self.title_var, 0)
        self._field(form, "发布时间", self.date_var, 1, padx=(12, 0))
        self._field(form, "固定路径 SLUG", self.slug_var, 2, padx=(12, 0))

        editor_head = ttk.Frame(content, style="App.TFrame")
        editor_head.pack(fill=X, pady=(0, 6))
        ttk.Label(editor_head, text="MARKDOWN 正文", style="Field.TLabel").pack(side=LEFT)
        self.dirty_label = ttk.Label(editor_head, text="已保存", style="Hint.TLabel")
        self.dirty_label.pack(side=RIGHT)

        text_wrap = tk.Frame(content, bg=RULE, bd=0, highlightthickness=1,
                             highlightbackground=RULE, highlightcolor=DUCK_EGG)
        text_wrap.pack(fill=BOTH, expand=True)
        self.body_text = tk.Text(
            text_wrap,
            wrap="word",
            undo=True,
            maxundo=-1,
            bg=PANEL_RAISED,
            fg=PAPER,
            insertbackground=DUCK_EGG,
            selectbackground="#365046",
            selectforeground=PAPER,
            relief="flat",
            padx=22,
            pady=18,
            spacing1=2,
            spacing3=5,
            font=(MONO_FONT, 11),
        )
        body_scroll = ttk.Scrollbar(text_wrap, orient="vertical", command=self.body_text.yview)
        self.body_text.configure(yscrollcommand=body_scroll.set)
        self.body_text.pack(side=LEFT, fill=BOTH, expand=True)
        body_scroll.pack(side=RIGHT, fill=Y)

        actions = ttk.Frame(content, style="App.TFrame")
        actions.pack(fill=X, pady=(14, 0), side=tk.BOTTOM, before=text_wrap)
        self.save_button = ttk.Button(actions, text="保存修改  Ctrl+S", style="Primary.TButton",
                                      command=self.save_current)
        self.save_button.pack(side=LEFT)
        self.publish_button = ttk.Button(actions, text="发布文章", style="Secondary.TButton",
                                         command=self.toggle_publish)
        self.publish_button.pack(side=LEFT, padx=(8, 0))
        ttk.Button(actions, text="打开线上文章", style="Secondary.TButton",
                   command=self.open_online).pack(side=LEFT, padx=(8, 0))
        ttk.Button(actions, text="打开文件位置", style="Secondary.TButton",
                   command=self.open_source_folder).pack(side=LEFT, padx=(8, 0))
        ttk.Button(actions, text="删除", style="Danger.TButton",
                   command=self.delete_current).pack(side=RIGHT)

    def _field(self, parent: ttk.Frame, label: str, variable: StringVar,
               column: int, padx: tuple[int, int] = (0, 0)) -> None:
        frame = ttk.Frame(parent, style="App.TFrame")
        frame.grid(row=0, column=column, sticky="ew", padx=padx)
        ttk.Label(frame, text=label, style="Field.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Entry(frame, textvariable=variable).pack(fill=X)

    def _build_footer(self) -> None:
        footer = ttk.Frame(self.editor, style="Panel.TFrame", height=58)
        footer.pack(fill=X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        status = ttk.Frame(footer, style="Panel.TFrame")
        status.pack(side=LEFT, fill=Y, padx=(34, 0))
        ttk.Label(status, text="PUBLISH PIPELINE", style="Eyebrow.TLabel").pack(anchor="w", pady=(9, 1))
        ttk.Label(status, textvariable=self.footer_status_var, style="Footer.TLabel").pack(anchor="w")

        self.sync_progress = ttk.Progressbar(footer, mode="indeterminate", length=110,
                                             style="Sync.Horizontal.TProgressbar")
        self.sync_progress.pack(side=RIGHT, padx=(10, 14))
        self.sync_button = ttk.Button(footer, text="提交并同步到 GitHub", style="Primary.TButton",
                                      command=self.sync_to_github)
        self.sync_button.pack(side=RIGHT)
        ttk.Button(footer, text="内容检查", style="Secondary.TButton",
                   command=self.run_content_check).pack(side=RIGHT, padx=(0, 9))

    def _bind_events(self) -> None:
        self.search_var.trace_add("write", lambda *_: self.refresh_tree())
        self.filter_var.trace_add("write", lambda *_: self.refresh_tree())
        for variable in (self.title_var, self.date_var, self.slug_var):
            variable.trace_add("write", lambda *_: self.mark_dirty())
        self.article_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.body_text.bind("<<Modified>>", self.on_body_modified)
        self.bind_all("<Control-s>", lambda _event: self.save_current())
        self.bind_all("<Control-n>", lambda _event: self.new_draft())
        self.bind_all("<Control-o>", lambda _event: self.import_markdown())

    def load_article_data(self) -> list[Article]:
        result: list[Article] = []
        for path in blog.iter_documents(include_drafts=True):
            try:
                metadata, body = blog.read_document(path)
                state = "draft" if path.parent == blog.DRAFTS_DIR else "published"
                date_value = blog.format_datetime(blog.parse_datetime(metadata.get("date")))
                slug = str(metadata.get("slug") or blog.clean_slug(path.stem))
                title = str(metadata.get("title") or blog.extract_title(body, path.stem))
                result.append(Article(path, metadata, body, state, title, date_value, slug))
            except Exception as exc:
                self.footer_status_var.set(f"跳过无法读取的文件：{path.name} · {exc}")
        result.sort(key=lambda item: item.date, reverse=True)
        return result

    def reload_articles(self, select_slug: str | None = None, select_first: bool = False) -> None:
        self.articles = self.load_article_data()
        published = sum(1 for article in self.articles if article.state == "published")
        drafts = len(self.articles) - published
        self.stats_var.set(f"{published} 篇已发布 · {drafts} 篇草稿")
        self.refresh_tree()

        target_iid = None
        if select_slug:
            for iid, article in self.article_by_iid.items():
                if article.slug == select_slug:
                    target_iid = iid
                    break
        if target_iid is None and select_first:
            children = self.article_tree.get_children()
            target_iid = children[0] if children else None
        if target_iid:
            self.article_tree.selection_set(target_iid)
            self.article_tree.focus(target_iid)
            self.article_tree.see(target_iid)
            self.show_article(self.article_by_iid[target_iid])
        elif not self.articles:
            self.clear_editor()

    def refresh_tree(self) -> None:
        selected_slug = self.current.slug if self.current else self.slug_var.get().strip()
        for iid in self.article_tree.get_children():
            self.article_tree.delete(iid)
        self.article_by_iid.clear()

        query = self.search_var.get().strip().casefold()
        selected_filter = self.filter_var.get()
        for index, article in enumerate(self.articles):
            if selected_filter != "all" and article.state != selected_filter:
                continue
            haystack = f"{article.title} {article.slug} {article.body}".casefold()
            if query and query not in haystack:
                continue
            iid = f"article-{index}"
            state_text = "发布" if article.state == "published" else "草稿"
            date_text = article.date[:10]
            self.article_tree.insert("", END, iid=iid, text=article.title,
                                     values=(state_text, date_text), tags=(article.state,))
            self.article_by_iid[iid] = article
            if selected_slug and article.slug == selected_slug:
                self.article_tree.selection_set(iid)

    def on_tree_select(self, _event: tk.Event) -> None:
        selection = self.article_tree.selection()
        if not selection:
            return
        article = self.article_by_iid.get(selection[0])
        if not article or (self.current_path and article.path == self.current_path):
            return
        if self.dirty and not self.confirm_discard_or_save():
            self._restore_tree_selection()
            return
        self.show_article(article)

    def _restore_tree_selection(self) -> None:
        if not self.current_path:
            return
        for iid, article in self.article_by_iid.items():
            if article.path == self.current_path:
                self.after_idle(lambda: self.article_tree.selection_set(iid))
                break

    def confirm_discard_or_save(self) -> bool:
        answer = messagebox.askyesnocancel(
            "未保存的修改",
            "当前文章还有未保存的修改。\n\n是：保存后继续\n否：放弃修改\n取消：留在当前文章",
            parent=self,
        )
        if answer is None:
            return False
        if answer:
            return self.save_current()
        self.set_dirty(False)
        return True

    def show_article(self, article: Article) -> None:
        self.loading = True
        self.current = article
        self.current_path = article.path
        self.current_metadata = dict(article.metadata)
        self.title_var.set(article.title)
        self.date_var.set(article.date)
        self.slug_var.set(article.slug)
        self.article_state_var.set(article.state)
        self.body_text.delete("1.0", END)
        self.body_text.insert("1.0", article.body.rstrip() + "\n")
        self.body_text.edit_modified(False)
        self.loading = False
        self.set_dirty(False)
        self.update_state_controls()
        self.footer_status_var.set(str(article.path.relative_to(blog.ROOT)))

    def clear_editor(self) -> None:
        self.loading = True
        self.current = None
        self.current_path = None
        self.current_metadata = {}
        self.title_var.set("")
        self.slug_var.set("")
        self.date_var.set(blog.format_datetime(datetime.now(blog.CHINA_TZ)))
        self.article_state_var.set("draft")
        self.body_text.delete("1.0", END)
        self.body_text.edit_modified(False)
        self.loading = False
        self.set_dirty(False)
        self.update_state_controls()

    def on_body_modified(self, _event: tk.Event) -> None:
        if self.body_text.edit_modified():
            self.mark_dirty()
            self.body_text.edit_modified(False)

    def mark_dirty(self) -> None:
        if not self.loading:
            self.set_dirty(True)

    def set_dirty(self, value: bool) -> None:
        self.dirty = value
        self.dirty_label.configure(text="有未保存修改" if value else "已保存")
        self.title(f"{'● ' if value else ''}{APP_NAME}")

    def update_state_controls(self) -> None:
        draft = self.article_state_var.get() == "draft"
        self.state_chip.configure(
            text="草稿" if draft else "已发布",
            bg=WARNING if draft else DUCK_EGG,
        )
        self.publish_button.configure(text="发布文章" if draft else "转为草稿")

    def new_draft(self) -> None:
        if self.dirty and not self.confirm_discard_or_save():
            return
        title = simpledialog.askstring("新建草稿", "文章标题", parent=self)
        if not title or not title.strip():
            return
        base_slug = blog.clean_slug(title)
        slug = base_slug
        index = 2
        while blog.find_by_slug(slug):
            slug = f"{base_slug}-{index}"
            index += 1

        self.clear_editor()
        self.loading = True
        self.title_var.set(title.strip())
        self.slug_var.set(slug)
        self.date_var.set(blog.format_datetime(datetime.now(blog.CHINA_TZ)))
        self.article_state_var.set("draft")
        self.body_text.insert("1.0", "从这里开始写作。\n")
        self.body_text.edit_modified(False)
        self.loading = False
        self.set_dirty(True)
        self.update_state_controls()
        self.footer_status_var.set("新草稿 · 尚未写入磁盘")
        self.body_text.focus_set()

    def import_markdown(self) -> None:
        if self.dirty and not self.confirm_discard_or_save():
            return
        source = filedialog.askopenfilename(
            parent=self,
            title="选择 Markdown 文章",
            filetypes=(("Markdown", "*.md *.markdown"), ("所有文件", "*.*")),
        )
        if not source:
            return
        as_draft = messagebox.askyesnocancel(
            "导入方式",
            "是否先导入为草稿？\n\n是：保存到草稿箱\n否：直接设为已发布\n取消：停止导入",
            parent=self,
        )
        if as_draft is None:
            return
        try:
            target = blog.add_document(Path(source), draft=as_draft, import_images=True)
            metadata, _ = blog.read_document(target)
            self.reload_articles(select_slug=str(metadata.get("slug")))
            self.footer_status_var.set(f"已导入 · {target.relative_to(blog.ROOT)}")
        except Exception as exc:
            messagebox.showerror("导入失败", str(exc), parent=self)

    def save_current(self) -> bool:
        title = self.title_var.get().strip()
        raw_slug = self.slug_var.get().strip()
        body = self.body_text.get("1.0", "end-1c")
        if not title:
            messagebox.showwarning("缺少标题", "请填写文章标题。", parent=self)
            return False
        try:
            slug = blog.clean_slug(raw_slug or title)
            published_at = blog.parse_datetime(self.date_var.get())
        except Exception as exc:
            messagebox.showerror("信息有误", str(exc), parent=self)
            return False

        duplicate = blog.find_by_slug(slug)
        if duplicate and (not self.current_path or duplicate.resolve() != self.current_path.resolve()):
            messagebox.showerror("路径重复", f"slug “{slug}” 已被另一篇文章使用。", parent=self)
            return False

        state = self.article_state_var.get()
        target_dir = blog.DRAFTS_DIR if state == "draft" else blog.POSTS_DIR
        target_name = f"{slug}.md" if state == "draft" else f"{published_at:%Y-%m-%d}-{slug}.md"
        target = target_dir / target_name
        if target.exists() and (not self.current_path or target.resolve() != self.current_path.resolve()):
            messagebox.showerror("文件已存在", f"目标文件已存在：{target.name}", parent=self)
            return False

        metadata = dict(self.current_metadata)
        metadata.update({
            "title": title,
            "date": blog.format_datetime(published_at),
            "slug": slug,
            "permalink": f"/post/{slug}.html",
        })
        metadata.pop("layout", None)

        old_slug = self.current.slug if self.current else None
        old_path = self.current_path
        if old_slug and old_slug != slug:
            old_assets = blog.POST_ASSETS_DIR / old_slug
            new_assets = blog.POST_ASSETS_DIR / slug
            if old_assets.exists():
                if new_assets.exists():
                    messagebox.showerror("图片目录冲突", f"已存在图片目录 assets/posts/{slug}", parent=self)
                    return False
                shutil.move(str(old_assets), str(new_assets))
            body = body.replace(f"/assets/posts/{old_slug}/", f"/assets/posts/{slug}/")

        try:
            blog.write_document(target, metadata, body)
            if old_path and old_path.exists() and old_path.resolve() != target.resolve():
                old_path.unlink()
        except Exception as exc:
            messagebox.showerror("保存失败", str(exc), parent=self)
            return False

        self.set_dirty(False)
        self.reload_articles(select_slug=slug)
        self.footer_status_var.set(f"已保存 · {target.relative_to(blog.ROOT)}")
        return True

    def toggle_publish(self) -> None:
        if not self.title_var.get().strip():
            return
        if self.article_state_var.get() == "draft":
            if not messagebox.askyesno(
                "发布文章",
                "将这篇文章标记为已发布？\n\n保存后它会进入 _posts，并在下次 GitHub Pages 构建时出现在首页。",
                parent=self,
            ):
                return
            self.article_state_var.set("published")
            self.date_var.set(blog.format_datetime(datetime.now(blog.CHINA_TZ)))
        else:
            if not messagebox.askyesno(
                "转为草稿",
                "将这篇文章从网站撤下并转入草稿箱？\n\n同步到 GitHub 后，线上首页会自动移除它。",
                parent=self,
            ):
                return
            self.article_state_var.set("draft")
        self.update_state_controls()
        self.set_dirty(True)
        self.save_current()

    def delete_current(self) -> None:
        if not self.current_path or not self.current_path.exists():
            messagebox.showinfo("没有可删除的文章", "请先从左侧选择一篇已保存文章。", parent=self)
            return
        slug = self.slug_var.get().strip()
        assets = blog.POST_ASSETS_DIR / slug
        asset_note = "\n对应的文章图片目录也会一并删除。" if assets.exists() else ""
        if not messagebox.askyesno(
            "确认删除",
            f"确定删除《{self.title_var.get().strip()}》吗？{asset_note}\n\n此操作会修改本地文件，但不会立即推送到 GitHub。",
            icon="warning",
            parent=self,
        ):
            return
        try:
            self.current_path.unlink()
            if assets.exists():
                shutil.rmtree(assets)
        except Exception as exc:
            messagebox.showerror("删除失败", str(exc), parent=self)
            return
        self.current = None
        self.current_path = None
        self.reload_articles(select_first=True)
        self.footer_status_var.set("文章已从本地删除 · 同步 GitHub 后线上生效")

    def open_online(self) -> None:
        slug = self.slug_var.get().strip()
        if not slug:
            return
        url = f"{SITE_URL}/post/{quote(slug)}.html"
        webbrowser.open(url)

    def open_source_folder(self) -> None:
        target = self.current_path.parent if self.current_path else blog.ROOT
        if os.name == "nt":
            os.startfile(target)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", str(target)])

    def run_content_check(self) -> None:
        if self.dirty and not self.save_current():
            return
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = blog.command_check(None)  # type: ignore[arg-type]
        output = stream.getvalue().strip() or "检查完成。"
        if code == 0:
            messagebox.showinfo("内容检查通过", output, parent=self)
            self.footer_status_var.set("内容检查通过 · 可以同步到 GitHub")
        else:
            messagebox.showerror("内容检查发现问题", output, parent=self)

    def sync_to_github(self) -> None:
        if self.git_busy:
            return
        if self.dirty and not self.save_current():
            return
        if not (blog.ROOT / ".git").exists():
            messagebox.showerror("不是 Git 仓库", f"{blog.ROOT} 中没有找到 .git。", parent=self)
            return
        if not messagebox.askyesno(
            "同步到 GitHub",
            "程序将只暂存博客文章、图片、样式、模板和管理工具，随后创建提交并推送。\n\n项目中的其他目录不会被加入这次提交。是否继续？",
            parent=self,
        ):
            return
        default_message = f"publish: {datetime.now(blog.CHINA_TZ):%Y-%m-%d %H:%M}"
        commit_message = simpledialog.askstring(
            "提交说明",
            "这次发布的 Git 提交说明：",
            initialvalue=default_message,
            parent=self,
        )
        if not commit_message or not commit_message.strip():
            return

        self.git_busy = True
        self.sync_button.configure(state="disabled")
        self.sync_progress.start(12)
        self.footer_status_var.set("正在检查并同步 GitHub…")
        threading.Thread(
            target=self._git_sync_worker,
            args=(commit_message.strip(),),
            daemon=True,
        ).start()

    def _run_git(self, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
        command = ["git", "-c", f"safe.directory={blog.ROOT}", "-C", str(blog.ROOT), *args]
        result = subprocess.run(
            command,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            startupinfo=hidden_startupinfo(),
        )
        if check and result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise RuntimeError(detail or f"git {' '.join(args)} 执行失败")
        return result

    def _git_sync_worker(self, commit_message: str) -> None:
        managed_paths = [
            "_posts", "_drafts", "assets", "_layouts", "_includes", "scripts",
            "index.html", "_config.yml", "README.md", "requirements.txt", "Gemfile",
            "CNAME", "view-counter.js", ".gitignore",
        ]
        try:
            self._run_git(["add", "-A", "--", *managed_paths])
            diff = self._run_git(["diff", "--cached", "--quiet"], check=False)
            if diff.returncode == 0:
                self.after(0, lambda: self._finish_git_sync(
                    True, "没有需要提交的博客改动。线上内容已是最新版本。"
                ))
                return
            if diff.returncode != 1:
                raise RuntimeError("无法检查待提交的博客改动。")
            self._run_git(["commit", "-m", commit_message])
            push = self._run_git(["push"])
            detail = (push.stdout or push.stderr).strip()
            message = "已提交并推送到 GitHub。GitHub Pages 将自动更新网站。"
            if detail:
                message += f"\n\n{detail}"
            self.after(0, lambda: self._finish_git_sync(True, message))
        except Exception as exc:
            self.after(0, lambda: self._finish_git_sync(False, str(exc)))

    def _finish_git_sync(self, success: bool, message: str) -> None:
        self.git_busy = False
        self.sync_progress.stop()
        self.sync_button.configure(state="normal")
        if success:
            self.footer_status_var.set("GitHub 同步完成 · Pages 正在自动部署")
            messagebox.showinfo("同步完成", message, parent=self)
        else:
            self.footer_status_var.set("GitHub 同步失败 · 本地内容没有丢失")
            messagebox.showerror("同步失败", message, parent=self)

    def on_close(self) -> None:
        if self.git_busy:
            if not messagebox.askyesno("同步仍在进行", "Git 同步还没有结束，确定退出吗？", parent=self):
                return
        if self.dirty and not self.confirm_discard_or_save():
            return
        self.destroy()


def main() -> int:
    if not (blog.ROOT / "_config.yml").exists():
        app = Tk()
        app.withdraw()
        messagebox.showerror(
            "无法找到博客项目",
            "请把 DuckLingBlogManager.exe 放在 blogweb 项目根目录后再运行。",
        )
        app.destroy()
        return 2
    BlogStudio().mainloop()
    return 0


def enable_dpi_awareness() -> None:
    if os.name != "nt":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        enable_dpi_awareness()
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        error_text = traceback.format_exc()
        error_root = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else blog.ROOT
        try:
            (error_root / "blog-manager-error.log").write_text(error_text, encoding="utf-8")
        except OSError:
            pass
        try:
            error_app = Tk()
            error_app.withdraw()
            messagebox.showerror(
                "DuckLing Blog Studio 启动失败",
                "程序启动时遇到错误。详情已写入 blog-manager-error.log。",
            )
            error_app.destroy()
        except Exception:
            pass
        raise
