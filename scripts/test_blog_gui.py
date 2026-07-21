"""Non-destructive smoke tests for DuckLing Blog Studio."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys
import subprocess
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import blog
import blog_gui


class BlogStudioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_paths = (
            blog.ROOT,
            blog.POSTS_DIR,
            blog.DRAFTS_DIR,
            blog.POST_ASSETS_DIR,
        )
        blog.ROOT = self.root
        blog.POSTS_DIR = self.root / "_posts"
        blog.DRAFTS_DIR = self.root / "_drafts"
        blog.POST_ASSETS_DIR = self.root / "assets" / "posts"
        blog.POSTS_DIR.mkdir()
        blog.DRAFTS_DIR.mkdir()
        (self.root / "_config.yml").write_text("title: Test\n", encoding="utf-8")
        blog.write_document(
            blog.DRAFTS_DIR / "sample.md",
            {
                "title": "示例草稿",
                "date": "2026-07-21 10:00:00 +0800",
                "slug": "sample",
                "permalink": "/post/sample.html",
            },
            "初始正文",
        )

    def tearDown(self) -> None:
        blog.ROOT, blog.POSTS_DIR, blog.DRAFTS_DIR, blog.POST_ASSETS_DIR = self.original_paths
        self.temp.cleanup()

    def test_save_publish_and_delete_cycle(self) -> None:
        app = blog_gui.BlogStudio()
        app.withdraw()
        app.update_idletasks()
        self.assertEqual(len(app.article_tree.get_children()), 1)
        self.assertEqual(app.article_state_var.get(), "draft")

        app.title_var.set("修改后的标题")
        app.body_text.delete("1.0", "end")
        app.body_text.insert("1.0", "修改后的正文")
        self.assertTrue(app.save_current())

        app.article_state_var.set("published")
        app.date_var.set("2026-07-22 08:30:00 +0800")
        self.assertTrue(app.save_current())
        published = blog.POSTS_DIR / "2026-07-22-sample.md"
        self.assertTrue(published.exists())
        self.assertFalse((blog.DRAFTS_DIR / "sample.md").exists())

        with patch.object(blog_gui.messagebox, "askyesno", return_value=True):
            app.delete_current()
        self.assertFalse(published.exists())
        app.destroy()

    def test_sync_pushes_existing_unpublished_commit(self) -> None:
        app = blog_gui.BlogStudio()
        app.withdraw()
        results = [
            subprocess.CompletedProcess([], 0, "", ""),  # git add
            subprocess.CompletedProcess([], 0, "", ""),  # no staged changes
            subprocess.CompletedProcess([], 0, "origin/main\n", ""),
            subprocess.CompletedProcess([], 0, "", ""),  # safe fast-forward
            subprocess.CompletedProcess([], 0, "", ""),  # push
        ]
        with patch.object(app, "_run_git", side_effect=results) as run_git:
            with patch.object(app, "_finish_git_sync"):
                app._git_sync_worker("publish: test")
                app.update()
        push_call = run_git.call_args_list[-1].args[0]
        self.assertEqual(push_call, ["push", "origin", "HEAD:main"])
        app.destroy()


if __name__ == "__main__":
    unittest.main()
