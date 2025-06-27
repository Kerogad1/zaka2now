import feedparser, os, re, json
from datetime import datetime

rss_feeds = {
    "Politics": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "Economy": "https://www.reuters.com/rssFeed/worldNews",
    "AI": "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
}

output_dir="articles"
os.makedirs(output_dir, exist_ok=True)

def slugify(text):
    return re.sub(r'\W+','-', text.strip().lower())

articles_list=[]

for cat, url in rss_feeds.items():
    feed=feedparser.parse(url)
    for entry in feed.entries[:5]:
        title=entry.title.split(' - ')[0]
        link=entry.link
        content=entry.summary if hasattr(entry,'summary') else ''
        # remove HTML tags
        summary=re.sub('<[^<]+?>','', content)[:500]+'...'
        slug=slugify(title)
        fname=f"{slug}.html"
        fpath=os.path.join(output_dir, fname)
        # optional image
        img_url=''
        if hasattr(entry,'media_content'):
            img_url=entry.media_content[0].get('url','')
        # write article file
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html lang='en'>
<head><meta charset='UTF-8'/><title>{title}</title></head>
<body>
  <h1>{title}</h1>
  {f"<img src='{img_url}' style='max-width:100%;'/><br/>" if img_url else ''}
  <p>{summary}</p>
  <p><a href='{link}'>Read more</a></p>
  <p><small>Updated: {datetime.now().strftime('%Y-%m-%d')}</small></p>
</body>
</html>""")
        articles_list.append({'title':title,'filename':fname,'summary':summary})

# write JSON index
with open(os.path.join(output_dir,'index.json'),'w',encoding='utf-8') as jf:
    json.dump({'articles':articles_list}, jf, ensure_ascii=False, indent=2)
