#!/usr/bin/env python3
"""DuckLing 博客的统一文章管理入口。

内容始终保存在 _posts/ 或 _drafts/。脚本只负责整理 Markdown、元信息
和本地图片，不生成文章 HTML；HTML 由 GitHub Pages/Jekyll 自动构建。
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import unquote

import yaml


def resolve_root() -> Path:
    """Locate the blog root both from source and from a frozen GUI executable."""
    if getattr(sys, "frozen", False):
        start = Path(sys.executable).resolve().parent
        candidates = (start, start.parent, Path.cwd().resolve())
    else:
        start = Path(__file__).resolve().parent
        candidates = (start.parent, start, Path.cwd().resolve())

    for candidate in candidates:
        if (candidate / "_config.yml").is_file() and (candidate / "_posts").is_dir():
            return candidate
    return start if getattr(sys, "frozen", False) else Path(__file__).resolve().parents[1]


ROOT = resolve_root()
POSTS_DIR = ROOT / "_posts"
DRAFTS_DIR = ROOT / "_drafts"
POST_ASSETS_DIR = ROOT / "assets" / "posts"
CHINA_TZ = timezone(timedelta(hours=8))

FRONT_MATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", re.S)
FIRST_H1_RE = re.compile(r"\A\s*#\s+(.+?)\s*(?:\r?\n|\Z)")
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[-_]?")
IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^\)]+)(\))")
INVALID_SLUG_CHARS_RE = re.compile(r"[<>:\"/\\|?*#%\x00-\x1f]")


class BlogError(RuntimeError):
    pass


def read_document(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8-sig")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise BlogError(f"Front matter 必须是对象: {path}")
    return metadata, text[match.end():]


def write_document(path: Path, metadata: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).strip()
    normalized_body = body.lstrip("\r\n").rstrip() + "\n"
    path.write_text(f"---\n{front}\n---\n\n{normalized_body}", encoding="utf-8")


def extract_title(body: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    if match:
        return re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
    return fallback


def strip_first_h1(body: str) -> str:
    return FIRST_H1_RE.sub("", body, count=1)


def clean_slug(value: str) -> str:
    value = DATE_PREFIX_RE.sub("", value.strip())
    value = INVALID_SLUG_CHARS_RE.sub("-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-. ")
    if not value:
        raise BlogError("无法从标题或文件名生成文章路径，请使用 --slug 指定")
    return value


def parse_datetime(value: Any, fallback: Optional[datetime] = None) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime(value.year, value.month, value.day)
    elif value:
        raw = str(value).strip()
        raw = raw.replace("Z", "+00:00")
        # Jekyll 常用 "YYYY-MM-DD HH:MM:SS +0800"，而 Python
        # fromisoformat 需要移除时区前的空格并补上冒号。
        raw = re.sub(r"\s+([+-]\d{2})(\d{2})$", r"\1:\2", raw)
        try:
            parsed = datetime.fromisoformat(raw)
        except ValueError:
            parsed = None
            for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    parsed = datetime.strptime(raw, fmt)
                    break
                except ValueError:
                    continue
            if parsed is None:
                raise BlogError(f"无法识别日期: {value}")
    elif fallback:
        parsed = fallback
    else:
        parsed = datetime.now(CHINA_TZ)

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=CHINA_TZ)
    return parsed.astimezone(CHINA_TZ)


def format_datetime(value: datetime) -> str:
    return value.astimezone(CHINA_TZ).strftime("%Y-%m-%d %H:%M:%S +0800")


def iter_documents(include_drafts: bool = True) -> Iterable[Path]:
    if POSTS_DIR.exists():
        yield from sorted(POSTS_DIR.glob("*.md"))
    if include_drafts and DRAFTS_DIR.exists():
        yield from sorted(DRAFTS_DIR.glob("*.md"))


def find_by_slug(slug: str, include_drafts: bool = True) -> Optional[Path]:
    for path in iter_documents(include_drafts):
        metadata, _ = read_document(path)
        if str(metadata.get("slug", "")) == slug:
            return path
    return None


def split_image_target(raw: str) -> tuple[str, str]:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        end = raw.index(">")
        return raw[1:end], raw[end + 1:]
    match = re.match(r"(\S+)(.*)", raw, re.S)
    return (match.group(1), match.group(2)) if match else (raw, "")


def import_local_images(source: Path, slug: str, body: str) -> tuple[str, int]:
    destination_root = POST_ASSETS_DIR / slug
    copied = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal copied
        target, suffix = split_image_target(match.group(2))
        if target.startswith(("http://", "https://", "data:", "/", "#")):
            return match.group(0)

        decoded = unquote(target)
        source_image = (source.parent / decoded).resolve()
        try:
            source_image.relative_to(source.parent.resolve())
        except ValueError:
            return match.group(0)
        if not source_image.is_file():
            return match.group(0)

        relative = Path(decoded)
        if relative.parts and relative.parts[0] == source.stem:
            relative = Path(*relative.parts[1:])
        if not relative.parts or ".." in relative.parts:
            relative = Path(source_image.name)

        destination = destination_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image, destination)
        copied += 1
        public_path = f"/assets/posts/{slug}/{relative.as_posix()}"
        return f"{match.group(1)}{public_path}{suffix}{match.group(3)}"

    return IMAGE_RE.sub(replace, body), copied


def add_document(
    source: Path,
    *,
    title: Optional[str] = None,
    slug: Optional[str] = None,
    published_at: Any = None,
    draft: bool = False,
    import_images: bool = True,
) -> Path:
    source = source.resolve()
    if not source.is_file():
        raise BlogError(f"Markdown 文件不存在: {source}")
    if source.suffix.lower() not in {".md", ".markdown"}:
        raise BlogError("只支持 .md 或 .markdown 文件")

    existing_metadata, body = read_document(source)
    resolved_title = title or existing_metadata.get("title") or extract_title(body, source.stem)
    resolved_slug = clean_slug(slug or existing_metadata.get("slug") or source.stem)
    duplicate = find_by_slug(resolved_slug)
    if duplicate and duplicate.resolve() != source:
        raise BlogError(f"文章路径已存在: {resolved_slug} ({duplicate.relative_to(ROOT)})")

    filename_date = DATE_PREFIX_RE.match(source.stem)
    fallback_date = None
    if filename_date:
        fallback_date = datetime.strptime(filename_date.group(1), "%Y-%m-%d").replace(tzinfo=CHINA_TZ)
    if fallback_date is None:
        fallback_date = datetime.fromtimestamp(source.stat().st_mtime, CHINA_TZ)
    resolved_date = parse_datetime(published_at or existing_metadata.get("date"), fallback_date)

    body = strip_first_h1(body)
    copied = 0
    if import_images:
        body, copied = import_local_images(source, resolved_slug, body)

    metadata = {
        "title": str(resolved_title).strip(),
        "date": format_datetime(resolved_date),
        "slug": resolved_slug,
        "permalink": f"/post/{resolved_slug}.html",
    }
    for key, value in existing_metadata.items():
        if key not in metadata and key != "layout":
            metadata[key] = value

    target_dir = DRAFTS_DIR if draft else POSTS_DIR
    filename = f"{resolved_slug}.md" if draft else f"{resolved_date:%Y-%m-%d}-{resolved_slug}.md"
    target = target_dir / filename
    write_document(target, metadata, body)
    if source.parent == DRAFTS_DIR and not draft and source != target:
        source.unlink()
    print(f"已添加: {target.relative_to(ROOT)}")
    if copied:
        print(f"已复制 {copied} 个本地图片到 assets/posts/{resolved_slug}/")
    return target


def command_new(args: argparse.Namespace) -> int:
    now = parse_datetime(args.date)
    slug = clean_slug(args.slug or args.title)
    temp = ROOT / f".{slug}.new.md"
    try:
        temp.write_text(f"# {args.title}\n\n在这里开始写作。\n", encoding="utf-8")
        target = add_document(temp, title=args.title, slug=slug, published_at=now, draft=args.draft)
    finally:
        if temp.exists():
            temp.unlink()
    print(f"编辑文件: {target}")
    return 0


def command_add(args: argparse.Namespace) -> int:
    add_document(
        Path(args.source),
        title=args.title,
        slug=args.slug,
        published_at=args.date,
        draft=args.draft,
        import_images=not args.no_images,
    )
    return 0


def command_list(args: argparse.Namespace) -> int:
    rows = []
    for path in iter_documents(include_drafts=args.drafts):
        metadata, body = read_document(path)
        is_draft = path.parent == DRAFTS_DIR
        rows.append((
            "草稿" if is_draft else "发布",
            str(metadata.get("date", "—"))[:16],
            str(metadata.get("slug", path.stem)),
            str(metadata.get("title") or extract_title(body, path.stem)),
        ))
    rows.sort(key=lambda row: row[1], reverse=True)
    if not rows:
        print("没有文章")
        return 0
    for state, published, slug, title in rows:
        print(f"{state}\t{published}\t{slug}\t{title}")
    print(f"\n共 {len(rows)} 篇")
    return 0


def command_edit(args: argparse.Namespace) -> int:
    path = find_by_slug(args.slug)
    if not path:
        raise BlogError(f"没有找到文章: {args.slug}")
    print(path)
    if args.print_only:
        return 0
    if args.editor:
        subprocess.run([args.editor, str(path)], check=False)
    elif os.name == "nt":
        os.startfile(path)  # type: ignore[attr-defined]
    elif os.environ.get("EDITOR"):
        subprocess.run([os.environ["EDITOR"], str(path)], check=False)
    else:
        print("未配置编辑器；请手动打开上面的文件路径。")
    return 0


def command_delete(args: argparse.Namespace) -> int:
    path = find_by_slug(args.slug)
    if not path:
        raise BlogError(f"没有找到文章: {args.slug}")
    if not args.yes:
        answer = input(f"确认删除 {path.relative_to(ROOT)}？[y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("已取消")
            return 0
    path.unlink()
    assets = POST_ASSETS_DIR / args.slug
    if assets.exists():
        shutil.rmtree(assets)
    print(f"已删除: {path.relative_to(ROOT)}")
    return 0


def command_publish(args: argparse.Namespace) -> int:
    path = find_by_slug(args.slug)
    if not path or path.parent != DRAFTS_DIR:
        raise BlogError(f"没有找到草稿: {args.slug}")
    metadata, body = read_document(path)
    published_at = parse_datetime(args.date)
    metadata["date"] = format_datetime(published_at)
    metadata["permalink"] = f"/post/{args.slug}.html"
    target = POSTS_DIR / f"{published_at:%Y-%m-%d}-{args.slug}.md"
    write_document(target, metadata, body)
    path.unlink()
    print(f"已发布: {target.relative_to(ROOT)}")
    return 0


def command_check(_args: argparse.Namespace) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[str, Path] = {}
    published_count = 0

    for path in iter_documents():
        metadata, body = read_document(path)
        relative = path.relative_to(ROOT)
        if path.parent == POSTS_DIR:
            published_count += 1
        for field in ("title", "date", "slug", "permalink"):
            if not metadata.get(field):
                errors.append(f"{relative}: 缺少 {field}")
        slug = str(metadata.get("slug", ""))
        if slug in seen:
            errors.append(f"{relative}: slug 与 {seen[slug].relative_to(ROOT)} 重复")
        elif slug:
            seen[slug] = path
        try:
            parse_datetime(metadata.get("date"))
        except BlogError as exc:
            errors.append(f"{relative}: {exc}")
        expected_permalink = f"/post/{slug}.html"
        if slug and metadata.get("permalink") != expected_permalink:
            warnings.append(f"{relative}: permalink 不是标准路径 {expected_permalink}")

        for match in IMAGE_RE.finditer(body):
            target, _ = split_image_target(match.group(2))
            if target.startswith("/assets/posts/"):
                asset = ROOT / unquote(target.lstrip("/"))
                if not asset.exists():
                    errors.append(f"{relative}: 图片不存在 {target}")

    for message in warnings:
        print(f"警告: {message}")
    for message in errors:
        print(f"错误: {message}")
    if errors:
        print(f"\n检查失败：{len(errors)} 个错误，{len(warnings)} 个警告")
        return 1
    print(f"检查通过：{published_count} 篇已发布文章，{len(seen) - published_count} 篇草稿，{len(warnings)} 个警告")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="管理 Jekyll Markdown 文章；不再手工生成 HTML 或维护 JSON。",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="列出文章")
    list_parser.add_argument("--drafts", action="store_true", help="同时显示草稿")
    list_parser.set_defaults(func=command_list)

    add_parser = subparsers.add_parser("add", help="导入一篇现有 Markdown")
    add_parser.add_argument("source", help="Markdown 文件路径")
    add_parser.add_argument("--title", help="覆盖从一级标题读取的标题")
    add_parser.add_argument("--date", help="发布时间，如 2026-07-21 22:30")
    add_parser.add_argument("--slug", help="固定文章路径标识")
    add_parser.add_argument("--draft", action="store_true", help="加入草稿目录")
    add_parser.add_argument("--no-images", action="store_true", help="不导入本地图片")
    add_parser.set_defaults(func=command_add)

    new_parser = subparsers.add_parser("new", help="新建 Markdown 文章")
    new_parser.add_argument("title", help="文章标题")
    new_parser.add_argument("--date", help="发布时间")
    new_parser.add_argument("--slug", help="固定文章路径标识")
    new_parser.add_argument("--draft", action="store_true", help="创建为草稿")
    new_parser.set_defaults(func=command_new)

    edit_parser = subparsers.add_parser("edit", help="打开已发布文章或草稿")
    edit_parser.add_argument("slug", help="文章 slug")
    edit_parser.add_argument("--editor", help="指定编辑器命令")
    edit_parser.add_argument("--print-only", action="store_true", help="仅输出文件路径")
    edit_parser.set_defaults(func=command_edit)

    delete_parser = subparsers.add_parser("delete", help="删除文章及其图片")
    delete_parser.add_argument("slug", help="文章 slug")
    delete_parser.add_argument("--yes", action="store_true", help="跳过确认，供自动化使用")
    delete_parser.set_defaults(func=command_delete)

    publish_parser = subparsers.add_parser("publish", help="把草稿移动到已发布文章")
    publish_parser.add_argument("slug", help="草稿 slug")
    publish_parser.add_argument("--date", help="发布时间，默认现在")
    publish_parser.set_defaults(func=command_publish)

    check_parser = subparsers.add_parser("check", help="检查元信息、重复路径和图片")
    check_parser.set_defaults(func=command_check)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except BlogError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
