import feedparser, os, re, json
from datetime import datetime
rss_feeds={'World':'https://rss.nytimes.com/services/xml/rss/nyt/World.xml','Technology':'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml','Economy':'https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml','AI':'https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en'}
os.makedirs('articles',exist_ok=True)
articles=[]
def slugify(t): return re.sub(r'\W+','-',t.strip().lower())
for cat,url in rss_feeds.items():
    feed=feedparser.parse(url)
    for e in feed.entries[:5]:
        title=e.title.split(' - ')[0]; link=e.link
        content=e.summary if hasattr(e,'summary') else ''
        summary=re.sub('<[^<]+>','',content)[:200]+'...'
        fn=slugify(title)+'.html'; path=os.path.join('articles',fn)
        with open(path,'w',encoding='utf-8') as f:
            f.write(f"<h1>{title}</h1><p>{summary}</p><p><a href='{link}'>Read more</a></p><small>{datetime.now().strftime('%Y-%m-%d')}</small>")
        articles.append({'title':title,'summary':summary,'filename':fn})
with open('articles/index.json','w',encoding='utf-8') as f: json.dump({'articles':articles},f,ensure_ascii=False)