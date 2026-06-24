#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章快速生成器 - 输入标题和关键词，生成JSON模板
用法:
  python add_article.py                          # 交互模式
  python add_article.py --title "标题" --kw "关键词" --cat image-circle
"""
import os, json, sys, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE_DIR = os.path.join(BASE_DIR, "articles")

CATEGORIES = [
    {"slug": "image-circle",    "name": "图片转圈修复"},
    {"slug": "image-send-fail", "name": "图片发送失败"},
    {"slug": "image-not-show",  "name": "图片无法显示"},
    {"slug": "album-permission","name": "相册权限设置"},
    {"slug": "media-optimize",  "name": "媒体加载优化"},
]

ICONS = ["\U0001f504", "\u26a0\ufe0f", "\U0001f4f7", "\u26a1", "\U0001f4e4", "\U0001f4e5", "\U0001f527", "\u2753", "\U0001f4be", "\U0001f4f1"]

def slugify(title):
    import re
    s = re.sub(r'[^\w\s-]', '', title.lower())
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return s

def create_template(title, keywords, category_slug, category_name, icon="\U0001f4d8"):
    today = datetime.date.today().isoformat()
    slug = "telegram-" + slugify(title)

    template = {
        "slug": slug,
        "category": category_slug,
        "category_name": category_name,
        "title": title,
        "subtitle": "",
        "meta_title": f"{title} | TG图片修复站",
        "description": f"本文介绍{title}的方法和步骤，覆盖Android和iOS设备。",
        "keywords": keywords,
        "date": today,
        "author": "TG图片修复站",
        "read_time": "5\u5206\u949f",
        "icon": icon,
        "sections": [
            {
                "type": "heading",
                "text": "\u4e00\u3001\u95ee\u9898\u73b0\u8c61"
            },
            {
                "type": "paragraph",
                "text": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u95ee\u9898\u73b0\u8c61\u7684\u63cf\u8ff0\u3002"
            },
            {
                "type": "heading",
                "text": "\u4e8c\u3001\u539f\u56e0\u5206\u6790"
            },
            {
                "type": "tip",
                "title": "\u539f\u56e01",
                "content": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u539f\u56e0\u8bf4\u660e\u3002",
                "color": "primary"
            },
            {
                "type": "heading",
                "text": "\u4e09\u3001\u89e3\u51b3\u6b65\u9aa4"
            },
            {
                "type": "steps",
                "steps": [
                    {"title": "\u6b65\u9aa41", "content": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u6b65\u9aa4\u8bf4\u660e\u3002"},
                    {"title": "\u6b65\u9aa42", "content": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u6b65\u9aa4\u8bf4\u660e\u3002"},
                    {"title": "\u6b65\u9aa43", "content": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u6b65\u9aa4\u8bf4\u660e\u3002"}
                ]
            },
            {
                "type": "heading",
                "text": "\u56db\u3001\u6ce8\u610f\u4e8b\u9879"
            },
            {
                "type": "paragraph",
                "text": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u6ce8\u610f\u4e8b\u9879\u3002"
            }
        ],
        "faq": [
            {
                "q": "\u5e38\u89c1\u95ee\u98981\uff1f",
                "a": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u56de\u7b54\u3002"
            },
            {
                "q": "\u5e38\u89c1\u95ee\u98982\uff1f",
                "a": "\u8bf7\u5728\u6b64\u5904\u586b\u5199\u56de\u7b54\u3002"
            }
        ]
    }
    return template

def interactive():
    print("=" * 50)
    print("  TG\u7ad9\u70b9 - \u6587\u7ae0\u5feb\u901f\u751f\u6210\u5668")
    print("=" * 50)

    title = input("\n\U0001f4dd \u6587\u7ae0\u6807\u9898: ").strip()
    if not title:
        print("\u274c \u6807\u9898\u4e0d\u80fd\u4e3a\u7a7a")
        return

    keywords = input("\U0001f50d \u5173\u952e\u8bcd (\u9017\u53f7\u5206\u9694): ").strip()
    if not keywords:
        keywords = title

    print("\n\U0001f4cb \u9009\u62e9\u5206\u7c7b:")
    for i, cat in enumerate(CATEGORIES):
        print(f"  {i+1}. {cat['name']} ({cat['slug']})")
    cat_choice = input("\u8f93\u5165\u5e8f\u53f7 (1-5): ").strip()
    try:
        cat_idx = int(cat_choice) - 1
        if cat_idx < 0 or cat_idx >= len(CATEGORIES):
            cat_idx = 0
    except ValueError:
        cat_idx = 0
    cat = CATEGORIES[cat_idx]

    print("\n\U0001f524 \u9009\u62e9\u56fe\u6807:")
    for i, icon in enumerate(ICONS):
        print(f"  {i+1}. {icon}")
    icon_choice = input("\u8f93\u5165\u5e8f\u53f7 (\u9ed8\u8ba41): ").strip()
    try:
        icon_idx = int(icon_choice) - 1 if icon_choice else 0
        if icon_idx < 0 or icon_idx >= len(ICONS):
            icon_idx = 0
    except ValueError:
        icon_idx = 0
    icon = ICONS[icon_idx]

    template = create_template(title, keywords, cat["slug"], cat["name"], icon)

    if not os.path.exists(ARTICLE_DIR):
        os.makedirs(ARTICLE_DIR)

    filename = template["slug"] + ".json"
    filepath = os.path.join(ARTICLE_DIR, filename)

    if os.path.exists(filepath):
        print(f"\n\u26a0\ufe0f \u6587\u4ef6\u5df2\u5b58\u5728: {filename}")
        overwrite = input("\u662f\u5426\u8986\u76d6? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("\u274c \u5df2\u53d6\u6d88")
            return

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"\n\u2705 \u5df2\u521b\u5efa: articles/{filename}")
    print(f"   \u5206\u7c7b: {cat['name']}")
    print(f"   \u56fe\u6807: {icon}")
    print(f"\n\U0001f4dd \u4e0b\u4e00\u6b65: \u7f16\u8f91\u8be5JSON\u6587\u4ef6\u586b\u5165\u5b9e\u9645\u5185\u5bb9")
    print(f"\U0001f504 \u7136\u540e\u8fd0\u884c: python build.py \u91cd\u65b0\u751f\u6210\u7ad9\u70b9")

def cli_mode():
    title = ""
    keywords = ""
    category_slug = "image-circle"
    icon = "\U0001f4d8"

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--title" and i+1 < len(args):
            title = args[i+1]; i += 2
        elif args[i] == "--kw" and i+1 < len(args):
            keywords = args[i+1]; i += 2
        elif args[i] == "--cat" and i+1 < len(args):
            category_slug = args[i+1]; i += 2
        elif args[i] == "--icon" and i+1 < len(args):
            icon = args[i+1]; i += 2
        else:
            i += 1

    if not title:
        interactive()
        return

    cat = next((c for c in CATEGORIES if c["slug"] == category_slug), CATEGORIES[0])
    if not keywords:
        keywords = title

    template = create_template(title, keywords, cat["slug"], cat["name"], icon)

    if not os.path.exists(ARTICLE_DIR):
        os.makedirs(ARTICLE_DIR)

    filepath = os.path.join(ARTICLE_DIR, template["slug"] + ".json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"\u2705 \u5df2\u521b\u5efa: articles/{template['slug']}.json")
    print(f"   \u8fd0\u884c python build.py \u91cd\u65b0\u751f\u6210\u7ad9\u70b9")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode()
    else:
        interactive()
