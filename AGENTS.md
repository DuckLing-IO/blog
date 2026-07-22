# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Mandatory workspace boundary

- The parent workspace is `D:\_MyBlog`.
- Codex may inspect, search, create, edit, or delete content only inside `D:\_MyBlog\blogweb` and `D:\_MyBlog\DuckLing-Blog`.
- Every other file and directory under `D:\_MyBlog` is out of scope: do not list it, read it, search it, or modify it.
- Keep all commands, tools, temporary files, and generated artifacts scoped to the two allowed directories above.
- If a future task appears to require access outside these directories, stop and ask the user for explicit permission before accessing it.
- Treat this boundary as a foundational project requirement that overrides ordinary repository-discovery habits.

## Skill usage

- Before starting a task, check the installed Codex skills and use every skill whose trigger and workflow match the request.
- Use `frontend-design` when creating a new interface or materially reshaping the site's visual design.
- Use `web-design-guidelines` when reviewing UI quality, accessibility, UX, or web best-practice compliance; fetch its current guideline source as required by that skill.
- Use `agent-browser` for real browser interaction, screenshots, website testing, exploratory QA, scraping, or browser automation; load the current CLI workflow before running browser commands.
- These named skills are important defaults, but they do not replace other installed skills that better match a future task.
- Follow each selected skill's `SKILL.md` instructions and continue to respect the mandatory workspace boundary above.

## Project overview

DuckLing's personal blog — a Jekyll static site deployed through GitHub Pages. Markdown in `_posts/` is the only published-content source. GitHub Pages rebuilds the shared layouts, homepage archive, and article pages after each push to `main`; there is no runtime server and no hand-maintained article registry.

## Repo structure (what matters)

```
blogweb/
├── _config.yml           # Jekyll and site settings
├── _layouts/             # Shared page skeletons; post.html serves every article
├── _includes/            # Shared header/navigation
├── _posts/               # Published Markdown source
├── _drafts/              # Unpublished Markdown source
├── assets/css/           # Shared site and article styling
├── assets/js/            # Small homepage search enhancement
├── assets/posts/         # Per-article local images
├── scripts/blog.py       # Unified list/add/new/edit/delete/check CLI
├── index.html            # Liquid homepage, generated from site.posts
├── view-counter.js       # Client-side view counter (calls Cloudflare Worker)
├── view-counter/         # Cloudflare Worker (KV-backed page view counter)
│   └── src/index.js
├── img/                  # Static images (avatar, favicon)
└── cpp/                  # C++ solution source files (unrelated to site)
```

## Key conventions

- Published files use `_posts/YYYY-MM-DD-slug.md` and YAML front matter.
- `slug` and `permalink: /post/<slug>.html` keep article URLs stable.
- The title, publication date, and path live with the Markdown, never in a central JSON/JS file.
- Per-article images live in `assets/posts/<slug>/` and are referenced with root-relative URLs.
- Do not commit generated `_site/` output; GitHub Pages produces it.
- Keep the current `/post/*.html` URL form because the view counter uses it as its stable key.

## Running locally

```bash
# Validate content metadata and image references
pip install -r requirements.txt
python scripts/blog.py check

# Import an existing note
python scripts/blog.py add path/to/note.md

# Local Jekyll preview (requires Ruby/Bundler)
bundle install
bundle exec jekyll serve --livereload
```
