import feedparser, os, re, json
from datetime import datetime
from transformers import pipeline

summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")
rss_feeds = {
    "Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
}
output_dir = "articles"
os.makedirs(output_dir, exist_ok=True)
article_list = []

def slugify(text): return re.sub(r'\W+', '-', text.strip().lower())

for cat, url in rss_feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:1]:
        title = entry.title.split(" - ")[0]
        content = entry.summary
        try:
            summary = summarizer(content, max_length=180, min_length=60, do_sample=False)[0]['summary_text']
        except:
            summary = content[:500]
        slug = slugify(title)
        file_name = f"{slug}.html"
        img_url = ''
        if hasattr(entry, 'media_content'):
            img_url = entry.media_content[0].get('url', '')
        elif hasattr(entry, 'enclosures'):
            img_url = entry.enclosures[0].get('href', '')
        article_list.append({
            "title": title, "filename": file_name,
            "summary": summary, "img_url": img_url
        })
        html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head><meta charset='UTF-8'><title>{title}</title></head>
<body>
<h1>{title}</h1>
<p>{summary}</p>
<a href='{entry.link}' target='_blank'>Read more</a>
<p><small>Updated on {datetime.now().strftime('%Y-%m-%d')}</small></p>
</body></html>"""
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
            f.write(html_content)

with open(os.path.join(output_dir, "index.json"), "w", encoding="utf-8") as f:
    json.dump(article_list, f, ensure_ascii=False, indent=2)