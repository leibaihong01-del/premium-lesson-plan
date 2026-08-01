# -*- coding: utf-8 -*-
"""知识更新监测：联网检查来源并提取正文级候选更新，离线自动降级。"""
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.memory import Memory


DEFAULTS = [
    {"name": "教育部职业教育与成人教育司", "domain": "职业教育政策", "url": "https://www.moe.gov.cn"},
    {"name": "中国城市轨道交通协会", "domain": "行业发展", "url": "https://www.camet.org.cn"},
    {"name": "职业教育国家教学标准", "domain": "国家教学标准", "url": "https://www.moe.gov.cn/s78/A07/"},
]
KEYWORDS = ["新政策", "新标准", "通知", "意见", "方案", "标准", "趋势"]


def extract_candidates(html_text, base_url):
    text = unescape(re.sub(r"<[^>]+>", " ", html_text))
    text = re.sub(r"\s+", " ", text)
    snippets = []
    for kw in KEYWORDS:
        for m in re.finditer(kw, text):
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 60)
            sn = text[start:end].strip()
            if sn not in snippets:
                snippets.append(sn)
            if len(snippets) >= 5:
                break
        if len(snippets) >= 5:
            break
    links = []
    for href, title in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html_text, re.S):
        t = unescape(re.sub(r"<[^>]+>", "", title)).strip()
        if t and any(k in t for k in KEYWORDS):
            links.append({"title": t[:80], "url": urllib.parse.urljoin(base_url, href)})
        if len(links) >= 5:
            break
    return snippets, links


def main():
    m = Memory()
    sources = m._load("knowledge_sources")
    if not isinstance(sources, list) or not sources:
        sources = DEFAULTS
    else:
        names = {s.get("name") for s in sources}
        for d in DEFAULTS:
            if d["name"] not in names:
                sources.append(dict(d))
    m._save("knowledge_sources", sources)
    rows = []
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    for s in sources:
        name = s.get("name", "")
        try:
            req = urllib.request.Request(s.get("url", ""), headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=10) as r:
                raw = r.read(50000)
                data = raw.decode("utf-8", "ignore")
                if "gb2312" in data[:2000].lower() or "gbk" in data[:2000].lower():
                    data = raw.decode("gb18030", "ignore")
                hits = [k for k in KEYWORDS if k in data]
                snippets, links = extract_candidates(data, s.get("url", ""))
                rows.append({"name": name, "status": "reachable", "hits": hits,
                             "links": links, "time": now})
                s["checked_at"] = now
                if links:
                    updates = m._load("knowledge_updates")
                    updates = updates if isinstance(updates, list) else []
                    for link in links:
                        updates.append({"domain": s.get("domain"), "source": name,
                                        "title": link["title"], "url": link["url"],
                                        "status": "candidate", "time": now})
                    m._save("knowledge_updates", updates)
        except Exception as exc:
            rows.append({"name": name, "status": "offline", "hits": [],
                         "links": [], "time": now, "error": str(exc)[:60]})
            s["checked_at"] = now
            s["offline"] = True
    m._save("knowledge_sources", sources)
    lines = ["# 知识监测状态报告", "", f"检查时间：{now}", ""]
    lines.append("| 来源 | 状态 | 命中关键词 | 候选更新 | 说明 |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        cand = "; ".join(l["title"] for l in r.get("links", []))[:120] or "-"
        lines.append(f"| {r['name']} | {r['status']} | {'、'.join(r['hits']) or '-'} | {cand} | {r.get('error', '')} |")
    offline = all(r["status"] == "offline" for r in rows)
    lines.append("")
    lines.append("说明：网络不可用时自动进入离线导入模式；候选更新已写入 memory/knowledge_updates，可经 core/knowledge_update.py 导入。")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "知识监测状态报告.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("监测模式:", "offline" if offline else "online", "| 报告:", out)


if __name__ == "__main__":
    main()
