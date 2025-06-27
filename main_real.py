
import feedparser
from datetime import datetime
from transformers import pipeline
import os
import re

# Arabic summarization pipeline
summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")

rss_feeds = {
    "سياسة": "https://www.france24.com/ar/tag/%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9/rss",
    "اقتصاد": "https://www.france24.com/ar/tag/%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF/rss",
    "تكنولوجيا": "https://www.france24.com/ar/tag/%D8%AA%D9%83%D9%86%D9%88%D9%84%D9%88%D8%AC%D9%8A%D8%A7/rss",
    "ذكاء اصطناعي": "https://news.google.com/rss/search?q=الذكاء+الاصطناعي&hl=ar&gl=EG&ceid=EG:ar"
}

output_dir = "articles"
os.makedirs(output_dir, exist_ok=True)

def slugify(text):
    return re.sub(r'\W+', '-', text.strip().lower())

for category, feed_url in rss_feeds.items():
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:3]:  # أو [:5] لو حابب
        title = entry.title
        link = entry.link
        content = entry.summary if hasattr(entry, 'summary') else ''
        try:
            summary = summarizer(content, max_length=130, min_length=50, do_sample=False)[0]['summary_text']
        except:
            summary = content[:300] + "..."

        slug = slugify(title)
        filename = os.path.join(output_dir, f"{slug}.html")
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
  <p><a href='{link}' target='_blank'>المصدر: {link}</a></p>
  <p><small>تم التحديث بتاريخ {datetime.now().strftime('%Y-%m-%d')}</small></p>
</body>
</html>""")
