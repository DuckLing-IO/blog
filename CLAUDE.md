# CLAUDE.md

This repository is a Jekyll blog deployed by GitHub Pages.

- Published content: `_posts/*.md`
- Drafts: `_drafts/*.md`
- Shared article layout: `_layouts/post.html`
- Shared styling: `assets/css/site.css` and `assets/css/post.css`
- Article management: `python scripts/blog.py --help`
- Content validation: `python scripts/blog.py check`

Do not recreate standalone article HTML or a central article JSON file. Keep each article's `slug` and `/post/<slug>.html` permalink stable because the view counter uses that path as its key.
