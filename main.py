
import datetime

# Simulate fetched articles
articles = [
    {
        "title": "📌 الذكاء الاصطناعي في مواجهة تغير المناخ",
        "summary": "AI يساعد الباحثين على التنبؤ بالكوارث الطبيعية ومعالجة البيانات البيئية بسرعة."
    },
    {
        "title": "📈 ارتفاع التضخم وتأثيره على الأسواق العربية",
        "summary": "تحليل AI يُظهر أن الارتفاع الأخير في التضخم يؤثر بشكل مباشر على الإنفاق الاستهلاكي في المنطقة."
    },
    {
        "title": "🤖 OpenAI تطلق GPT-5 بقدرات تحليلية أقوى",
        "summary": "النموذج الجديد يمكنه تلخيص الأخبار، وكتابة مقالات كاملة، وتقديم تحليلات اقتصادية دقيقة."
    }
]

# Generate the HTML file
html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Zaka2 Now - تحديث تلقائي</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>🧠 Zaka2 Now</h1>
        <nav>
            <a href="#">الرئيسية</a>
            <a href="#">سياسة</a>
            <a href="#">اقتصاد</a>
            <a href="#">تكنولوجيا</a>
            <a href="#">ذكاء صناعي</a>
        </nav>
    </header>
    <main>
        <section class="latest">
            <h2>📡 آخر تحديث: ''' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '''</h2>
'''

for article in articles:
    html += f"<article><h3>{article['title']}</h3><p>{article['summary']}</p></article>"

html += '''
        </section>
    </main>
    <footer>
        <p>© 2025 Zaka2 Now - يتم التحديث تلقائيًا كل 24 ساعة</p>
    </footer>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
