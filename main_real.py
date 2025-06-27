import feedparser
from datetime import datetime
from transformers import pipeline
import os
import re

summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")

rss_feeds = {
    "سياسة": "https://www.france24.com/ar/tag/سياسة/rss",
    "اقتصاد": "https://www.france24.com/ar/tag/اقتصاد/rss",
    "تكنولوجيا": "https://www.france24.com/ar/tag/تكنولوجيا/rss",
    "ذكاء اصطناعي": "https://news.google.com/rss/search?q=الذكاء+الاصطناعي&hl=ar&gl=EG&ceid=EG:ar"
}

output_dir = "articles"
os.makedirs(output_dir, exist_ok=True)
index_data = []

def slugify(text):
    return re.sub(r'\W+', '-', text.strip().lower())

for category, feed_url in rss_feeds.items():
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:1]:
        title = entry.title
        link = entry.link
        content = entry.summary if hasattr(entry, 'summary') else ''
        try:
            summary = summarizer(content, max_length=180, min_length=80, do_sample=False)[0]['summary_text']
        except:
            summary = content[:300] + "..."

        slug = slugify(title)
        filename = os.path.join(output_dir, f"{slug}.html")
        index_data.append({"title": title, "link": f"articles/{slug}.html", "summary": summary})

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang='ar' dir='rtl'>
<head>
  <meta charset='UTF-8'>
  <title>{title}</title>
  <style>
    body {{ font-family: Tahoma, sans-serif; padding: 20px; background-color: #f9f9f9; }}
    h1 {{ color: #1a1a1a; }}
    p {{ font-size: 18px; line-height: 1.7; }}
    a {{ color: #0077cc; text-decoration: none; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>{summary}</p>
  <p><a href='{link}' target='_blank'>المصدر</a></p>
  <p><small>تم التحديث بتاريخ {datetime.now().strftime('%Y-%m-%d')}</small></p>
</body>
</html>""")

with open(os.path.join(output_dir, "index.json"), "w", encoding="utf-8") as f:
    import json
    json.dump(index_data, f, ensure_ascii=False, indent=2)
