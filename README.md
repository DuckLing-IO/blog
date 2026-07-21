# DuckLing's Blog

## Windows 图形化文章管理器

`DuckLingBlogManager/DuckLingBlogManager.exe` 是统一的桌面管理入口。双击运行后可以：

- 搜索和筛选全部已发布文章与草稿；
- 新建草稿或导入现有 Markdown（本地图片会自动归档）；
- 修改标题、发布时间、固定链接和 Markdown 正文；
- 在草稿与已发布状态之间切换；
- 删除文章及其专属图片目录；
- 运行内容检查，并在确认后只提交博客相关文件到 GitHub。

“发布文章”会把 Markdown 移入 `_posts/`；“提交并同步到 GitHub”才会创建 Git 提交并推送，随后由 GitHub Pages 自动部署。GUI 不依赖常驻服务器，文章源文件仍可被其他项目直接复制或通过 `scripts/blog.py` 自动导入。

重新构建管理器：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_gui.ps1
```

一个部署在 GitHub Pages 的纯静态博客。Markdown 是唯一文章源；GitHub Pages 使用 Jekyll 在每次 push 后自动生成首页和文章页。

## 内容结构

```text
_posts/             已发布 Markdown
_drafts/            草稿，不会出现在网站
_layouts/post.html  全部文章共用的页面模板
assets/css/         全站字体、颜色与排版
assets/posts/       文章本地图片
scripts/blog.py     统一文章管理入口
```

`articles.js` 和逐篇 HTML 转换已经取消。首页直接读取 Jekyll 的 `site.posts`，按发布时间倒序生成。

## 发布新文章

最省事的方式是导入写好的 Markdown：

```powershell
python scripts/blog.py add "D:\notes\今天的学习笔记.md"
```

脚本会：

1. 从第一个 `# 一级标题` 读取文章标题；
2. 使用当前时间作为发布时间（也可读取现有 front matter）；
3. 生成固定的文章路径；
4. 复制 Markdown 引用的本地图片到 `assets/posts/<slug>/`；
5. 写入 `_posts/`，不生成 HTML、不修改 JSON。

需要明确时间或路径时：

```powershell
python scripts/blog.py add note.md --date "2026-07-21 22:30" --slug daily-note-2026-07-21
```

也可以新建一篇空白文章：

```powershell
python scripts/blog.py new "今天学到的三件事" --draft
```

确认内容后发布草稿：

```powershell
python scripts/blog.py publish today-learned
```

## 查看、修改和删除

```powershell
# 查看已发布文章和草稿
python scripts/blog.py list --drafts

# 打开文章（Windows 使用默认 Markdown 编辑器）
python scripts/blog.py edit daily-note-2026-07-21

# 将草稿正式发布（自动使用当前时间）
python scripts/blog.py publish daily-note-2026-07-21

# 删除文章及它在 assets/posts/ 下的图片
python scripts/blog.py delete daily-note-2026-07-21

# 发布前检查重复路径、元信息和缺失图片
python scripts/blog.py check
```

修改 `_posts/` 中任意 Markdown 后提交即可；删除对应文件后，文章会在下次 Pages 构建时从首页和站点中一起消失。

## 部署

仓库继续使用 GitHub Pages 的 `main` 分支根目录发布方式。Jekyll 是 GitHub Pages 的原生构建器，因此不需要项目内的长期服务器，也不需要额外维护 Actions 工作流。

```powershell
git add _posts _drafts assets
git commit -m "publish: 学习笔记"
git push
```

push 后 GitHub 自动执行 `pages-build-deployment`。站点仍使用 `CNAME` 中的 `blog.duckee.top`。

## 本地预览

安装 Ruby 后执行：

```powershell
bundle install
bundle exec jekyll serve --livereload
```

访问 `http://127.0.0.1:4000/`。只检查文章数据时无需 Ruby：

```powershell
pip install -r requirements.txt
python scripts/blog.py check
```

## 统一修改样式

- 全站颜色、字体、导航和首页：`assets/css/site.css`
- 文章正文、标题、表格和代码块：`assets/css/post.css`
- 文章页面结构：`_layouts/post.html`
- 全站 HTML 骨架：`_layouts/default.html`

修改后 push，GitHub Pages 会重新构建全部文章，旧文章不需要逐篇处理。

## 知识库项目接入

知识库每天生成笔记后，调用同一个导入命令即可：

```powershell
python D:\_MyBlog\blogweb\scripts\blog.py add "D:\knowledge\daily\2026-07-21.md" --slug "daily-2026-07-21"
python D:\_MyBlog\blogweb\scripts\blog.py check
```

然后由知识库项目或现有自动化完成 `git add / commit / push`。如果知识库能直接输出带 front matter 的文件，也可直接复制到 `_posts/`：

```yaml
---
title: 今天的学习笔记
date: 2026-07-21 22:30:00 +0800
slug: daily-2026-07-21
permalink: /post/daily-2026-07-21.html
---
```
