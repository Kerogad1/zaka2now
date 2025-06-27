
import feedparser
from datetime import datetime
from transformers import pipeline
import os
import re

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

all_articles = []

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

        all_articles.append({"title": title, "filename": filename, "category": category})

# Generate index.html
index_html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>Zaka Now - أخبارك اليومية</title>
  <style>
    body { font-family: Tahoma, sans-serif; padding: 20px; background-color: #fff; color: #333; }
    h1 { color: #1a1a1a; text-align: center; }
    h2 { color: #0077cc; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
    ul { list-style-type: none; padding: 0; }
    li { margin: 8px 0; }
    a { color: #cc0000; text-decoration: none; font-size: 18px; }
    footer { margin-top: 30px; text-align: center; font-size: 14px; color: #666; }
  </style>
</head>
<body>
  <h1>🌍 Zaka Now - أحدث الأخبار بتقنية الذكاء الاصطناعي</h1>
'''

categories = {}
for art in all_articles:
    categories.setdefault(art["category"], []).append(art)

for category, items in categories.items():
    index_html += f"<h2>{category}</h2><ul>"
    for art in items:
        index_html += f"<li><a href='articles/{art['filename']}'>{art['title']}</a></li>"
    index_html += "</ul>"

index_html += f"<footer>آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M')} بواسطة الذكاء الاصطناعي</footer></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
