import feedparser
from datetime import datetime
from transformers import pipeline
import os
import re

# Arabic summarization pipeline
summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")

rss_feeds = {
    "سياسة": "https://www.france24.com/ar/tag/سياسة/rss",
    "اقتصاد": "https://www.france24.com/ar/tag/اقتصاد/rss",
    "تكنولوجيا": "https://www.france24.com/ar/tag/تكنولوجيا/rss",
    "ذكاء اصطناعي": "https://news.google.com/rss/search?q=الذكاء+الاصطناعي&hl=ar&gl=EG&ceid=EG:ar"
}

output_dir = "articles"
os.makedirs(output_dir, exist_ok=True)

def slugify(text):
    return re.sub(r'\W+', '-', text.strip().lower())

article_links = []

for category, feed_url in rss_feeds.items():
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:1]:
        title = entry.title
        link = entry.link
        content = entry.summary if hasattr(entry, 'summary') else ''
        try:
            summary = summarizer(content, max_length=130, min_length=50, do_sample=False)[0]['summary_text']
        except:
            summary = content[:300] + "..."

        slug = slugify(title)
        filename = f"{slug}.html"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
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

        article_links.append((title, filename, summary))

# توليد ملف index.html داخل articles/
index_path = os.path.join(output_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang='ar' dir='rtl'>
<head>
  <meta charset='UTF-8'>
  <title>أحدث المقالات</title>
  <style>
    body {{ font-family: Tahoma, sans-serif; padding: 30px; background-color: #ffffff; }}
    h1 {{ color: #333; }}
    h3 {{ margin-top: 20px; }}
    p {{ color: #444; font-size: 16px; }}
    a {{ color: #0077cc; text-decoration: none; }}
  </style>
</head>
<body>
  <h1>أحدث المقالات</h1>
""")
    for title, filename, summary in article_links:
        f.write(f"<h3><a href='{filename}'>{title}</a></h3>\n<p>{summary}</p>\n<hr/>\n")
    f.write("</body>\n</html>")
