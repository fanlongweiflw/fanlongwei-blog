#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update blog article data from a Word .docx file.

Usage:
  python3 scripts/update-from-word.py "/path/to/个人blog.docx"
"""

from __future__ import annotations

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
ARTICLES_PATH = ROOT_DIR / "src" / "data" / "articles.ts"
IMAGE_DIR = ROOT_DIR / "public" / "blog-images"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
}

PHRASE_KEYWORDS = [
    "Claude Code", "Product taste", "Cat Wu", "HeyGen", "Sora2", "Sora", "可灵", "DiT架构",
    "Stable Diffusion", "FLUX Kontext", "Remini", "Krea", "Motiff", "Captions AI", "Vozo",
    "多邻国", "张小龙", "俞军", "张一鸣", "Adobe max", "Capsule Video", "ReLens", "MOKI",
    "FancyTech", "度咔剪辑", "Team Building", "AI产品", "AI时代", "大模型", "视频生成",
    "图像编辑", "AI绘画", "AI写真", "AI漫剧", "AI短剧", "AI续写", "AI聚合平台", "AIGC检测",
    "提示词", "Agent", "RAG", "基模", "多模态", "模型训练", "算力", "数据闭环", "技术平权",
    "应用爆发", "创作工具", "创作工作流", "视频剪辑", "口播视频", "文字成片", "图片转3D",
    "希区柯克变焦", "跳舞变装", "视频彩铃", "AI特效", "爆款方法论", "增长方法论", "MVP",
    "用户体验", "产品经理", "产品设计", "产品判断", "用户需求", "需求本质", "需求文档",
    "竞品思考", "业务指标", "功能价值", "目标用户", "客户反馈", "长期价值", "组织变革",
    "团队架构", "组织协作", "工作实践", "会议分层", "任务管理", "产品品味", "判断力",
    "洞察力", "简洁力", "长期主义", "本质思维", "商业安全", "商业化", "市场调研",
    "机会分析", "增长价值", "数据依赖", "产品逻辑", "开源项目", "独立开发者", "极简生活",
    "用户心智", "设计原理", "文档写作", "产品方法论", "创新需求", "复杂需求", "Good Case",
    "Bad Case", "从领导学习", "体验复盘", "商单记录", "小红书IP", "美图影像节", "AI资讯",
    "产品观察", "技术趋势", "行业机会", "工具生态", "效率工具", "创作者", "内容生产",
    "科普视频", "电商场景", "教育场景", "游戏场景", "组织速度", "角色收敛", "人机协作",
    "决策负担", "AI采访", "业务懂行", "垂直场景", "产品机会", "加载体验", "假进度条",
    "导出体验", "用户反馈", "AB实验", "算法优化", "效果需求", "交互细节", "产品价值",
    "用户视角", "PM视角", "需求评审", "剪映", "快影", "抖音", "快手", "小红书", "视频号",
    "TikTok", "TT增长", "互联网产品", "大厂项目", "钉钉ONE", "组织内耗", "短期政绩",
    "养人型工作", "耗人型工作", "系统背景", "代码审查", "安全合规", "原型先行", "文档后置",
    "自动化", "AI工具", "一个人团队", "AI创新工作室",
]

FALLBACK_BY_CATEGORY = {
    "AI": ["AI产品", "技术趋势", "产品判断", "行业机会"],
    "产品": ["产品设计", "用户需求", "产品判断", "用户体验"],
    "创作": ["创作工具", "内容生产", "视频创作", "用户体验"],
    "工作": ["工作实践", "组织协作", "长期思考", "方法论"],
    "思考": ["产品观察", "长期思考", "判断力", "方法论"],
}

SPECIFIC_KEYWORDS = {
    "抖音/快手/小红书/视频号 AI 爆款内容特征分析": ["爆款内容", "平台差异", "AIGC内容", "内容分发"],
    "几个玩法类效果": ["玩法效果", "创作灵感", "视频特效", "体验记录"],
    "The First": ["个人起点", "产品记录", "长期写作", "第一篇笔记"],
    "美图影像节PPT记录": ["美图影像节", "MOKI", "视频创作", "工作流"],
    "实践出真知": ["实践复盘", "经验沉淀", "产品判断", "行动学习"],
    "三句话总结核心设计原理": ["设计原理", "产品设计", "用户体验", "简洁表达"],
}

KEYWORD_OVERRIDES_BY_TITLE = {
    "HeyGen的产品增长方法论": ["HeyGen", "增长方法论", "MVP", "用户教育"],
    "如何理解业务和指标的关系": ["业务指标", "运营逻辑", "指标体系", "业务判断"],
    "大模型是如何训练的": ["大模型", "模型训练", "算力", "数据质量"],
    "Captions AI 又推出了一个很惊喜的功能 AI Edit": ["Captions AI", "AI Edit", "口播视频", "智能包装"],
    "强引导就一定能带来提升吗？": ["强引导", "用户行为", "体验验证", "产品实验"],
    "再小的细节，也应该基于产品逻辑思考": ["产品逻辑", "细节体验", "用户反馈", "价值判断"],
    "创新/复杂需求，前期方案设计和规划的思考": ["创新需求", "复杂需求", "方案规划", "前期设计"],
    "度咔剪辑-文字成片体验": ["度咔剪辑", "文字成片", "剪辑体验", "AI创作"],
}

DATE_OVERRIDES_BY_TITLE = {
    "快手竟然做出了可灵？从这件事情我可以学到什么": "2026-06-11",
}


def slugify(title: str, index: int, date: str) -> str:
    words = re.sub(r"^[\d\.A-Za-z\s]+", "", title.strip().lower())
    words = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", words).strip("-")[:48]
    return f"{date}-{words}" if words and re.match(r"^\d{4}-\d{2}-\d{2}$", date) else f"post-{index:02d}-{words}"


def parse_date(raw_title: str, clean_title_value: str) -> str:
    if clean_title_value in DATE_OVERRIDES_BY_TITLE:
        return DATE_OVERRIDES_BY_TITLE[clean_title_value]

    match = re.match(r"^(\d{2})\.(\d{2})\.(\d{1,3})", raw_title.strip())
    if match:
        day = int(match.group(3))
        return f"20{match.group(1)}-{match.group(2)}-{day:02d}"

    year = re.match(r"^(\d{2})\.", raw_title.strip())
    return f"20{year.group(1)}" if year else "未标注"


def clean_title(raw_title: str) -> str:
    return re.sub(r"^\d{2}\.[\dA-Z]{1,3}\.?\d{0,3}\s*", "", raw_title).strip() or raw_title.strip()


def category_for(title: str, body: str) -> str:
    text = title + " " + body[:500]
    if any(k in text for k in ["AI", "大模型", "Claude", "Sora", "生成", "AIGC", "可灵", "GPT", "模型", "智能"]):
        return "AI"
    if any(k in text for k in ["产品", "需求", "用户", "体验", "PM", "设计", "指标"]):
        return "产品"
    if any(k in text for k in ["创作", "剪辑", "视频", "短剧", "影像", "内容"]):
        return "创作"
    if any(k in text for k in ["组织", "团队", "工作", "会议", "leader", "管理"]):
        return "工作"
    return "思考"


def add_keyword(items: list[str], keyword: str) -> None:
    keyword = keyword.strip(' ，。、：:；;（）()《》“”"')
    if not keyword or keyword in {"AI", "PM"}:
        return
    if len(keyword) > 12 and not re.search(r"[A-Za-z]", keyword):
        return
    if keyword not in items:
        items.append(keyword)


def split_title(title: str) -> list[str]:
    clean = re.sub(r"^[\d\.A-Za-z\s]+", "", title)
    clean = re.sub(r"[，。！？、：:；;（）()《》“”\"/]+", " ", clean)
    return [part.strip() for part in clean.split() if 2 <= len(part.strip()) <= 12]


def infer_keywords(article: dict) -> list[str]:
    title = article["title"]
    if title in KEYWORD_OVERRIDES_BY_TITLE:
        return KEYWORD_OVERRIDES_BY_TITLE[title]

    body = title + " " + article.get("excerpt", "") + " " + " ".join(
        block.get("text", "") for block in article.get("blocks", []) if block.get("type") == "paragraph"
    )[:1600]
    keywords: list[str] = []

    for key, values in SPECIFIC_KEYWORDS.items():
        if key in title:
            for value in values:
                add_keyword(keywords, value)

    for phrase in PHRASE_KEYWORDS:
        if phrase.lower() in body.lower():
            add_keyword(keywords, phrase)

    for part in split_title(title):
        if len(keywords) < 6:
            add_keyword(keywords, part)

    if "AI时代" in keywords and "AI产品" not in keywords and ("产品" in body or "产品经理" in body):
        add_keyword(keywords, "AI产品")
    if "产品经理" in body and "产品判断" not in keywords:
        add_keyword(keywords, "产品判断")
    if "用户" in body and "用户需求" not in keywords and "用户体验" not in keywords:
        add_keyword(keywords, "用户需求")
    if "视频" in body and "视频创作" not in keywords and "视频生成" not in keywords:
        add_keyword(keywords, "视频创作")
    if "需求" in body and "需求分析" not in keywords and "用户需求" not in keywords:
        add_keyword(keywords, "需求分析")

    for fallback in FALLBACK_BY_CATEGORY.get(article.get("category"), FALLBACK_BY_CATEGORY["思考"]):
        add_keyword(keywords, fallback)

    cleaned: list[str] = []
    for keyword in keywords:
        if len(keyword) > 10 and not re.search(r"[A-Za-z]", keyword):
            continue
        if keyword not in cleaned:
            cleaned.append(keyword)
        if len(cleaned) == 4:
            break

    while len(cleaned) < 4:
        for fallback in ["产品观察", "用户需求", "判断力", "长期思考"]:
            if fallback not in cleaned:
                cleaned.append(fallback)
                break

    return cleaned[:4]


def extract_articles(docx_path: Path) -> list[dict]:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(docx_path) as archive:
        names = archive.namelist()
        rel_root = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        rels = {rel.attrib.get("Id"): rel.attrib.get("Target") for rel in rel_root}
        document_root = ET.fromstring(archive.read("word/document.xml"))

        blocks = []
        referenced_images: set[str] = set()
        for paragraph in document_root.findall(".//w:body/w:p", NS):
            text = "".join(text_node.text or "" for text_node in paragraph.findall(".//w:t", NS)).strip()
            style = ""
            paragraph_properties = paragraph.find("w:pPr", NS)
            if paragraph_properties is not None:
                paragraph_style = paragraph_properties.find("w:pStyle", NS)
                if paragraph_style is not None:
                    style = paragraph_style.attrib.get(f"{{{NS['w']}}}val", "")

            images = []
            for blip in paragraph.findall(".//a:blip", NS):
                relationship_id = blip.attrib.get(f"{{{NS['r']}}}embed") or blip.attrib.get(f"{{{NS['r']}}}link")
                if relationship_id and rels.get(relationship_id):
                    target = rels[relationship_id]
                    images.append(target)
                    referenced_images.add(target)

            for image_data in paragraph.findall(".//v:imagedata", NS):
                relationship_id = image_data.attrib.get(f"{{{NS['r']}}}id")
                if relationship_id and rels.get(relationship_id):
                    target = rels[relationship_id]
                    images.append(target)
                    referenced_images.add(target)

            if text or images:
                blocks.append({"style": style, "text": text, "images": images})

        raw_articles = []
        current = None
        for block in blocks:
            if block["style"] == "2" and block["text"]:
                if current:
                    raw_articles.append(current)
                current = {"title": block["text"], "blocks": []}
            elif current:
                if block["text"]:
                    current["blocks"].append({"type": "paragraph", "text": block["text"]})
                for image in block["images"]:
                    current["blocks"].append({"type": "image", "src": "/blog-images/" + Path(image).name})
        if current:
            raw_articles.append(current)

        for image in referenced_images:
            source = "word/" + image
            if source in names:
                (IMAGE_DIR / Path(image).name).write_bytes(archive.read(source))

    articles = []
    for index, raw_article in enumerate(raw_articles, 1):
        title = clean_title(raw_article["title"])
        date = parse_date(raw_article["title"], title)
        body_text = "\n".join(block["text"] for block in raw_article["blocks"] if block["type"] == "paragraph")
        images = [block["src"] for block in raw_article["blocks"] if block["type"] == "image"]
        excerpt = re.sub(r"\s+", " ", body_text).strip()[:128]
        word_count = len(re.sub(r"\s+", "", body_text))
        article = {
            "id": index,
            "slug": slugify(title, index, date),
            "rawTitle": raw_article["title"],
            "title": title,
            "date": date,
            "category": category_for(raw_article["title"], body_text),
            "excerpt": excerpt or "这是一篇仍在整理中的文章。",
            "wordCount": word_count,
            "readingTime": max(1, round(word_count / 450)),
            "hasImages": bool(images),
            "cover": images[0] if images else None,
            "blocks": raw_article["blocks"],
        }
        article["keywords"] = infer_keywords(article)
        articles.append(article)

    return articles


def write_articles(articles: list[dict]) -> None:
    output = (
        'import type { BlogArticle } from "../lib/types";\n\n'
        "export const articles: BlogArticle[] = "
        + json.dumps(articles, ensure_ascii=False, indent=2)
        + ";\n"
    )
    ARTICLES_PATH.write_text(output, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 scripts/update-from-word.py /path/to/blog.docx")

    docx_path = Path(sys.argv[1]).expanduser().resolve()
    if not docx_path.exists():
        raise SystemExit(f"Word file not found: {docx_path}")

    articles = extract_articles(docx_path)
    write_articles(articles)
    print(f"Updated {ARTICLES_PATH}")
    print(f"Articles: {len(articles)}")
    print(f"Referenced images in {IMAGE_DIR}: {len(list(IMAGE_DIR.glob('*')))}")
    print(f"Minimum keywords per article: {min(len(article['keywords']) for article in articles)}")


if __name__ == "__main__":
    main()
