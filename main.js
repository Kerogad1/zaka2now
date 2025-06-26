
// محاكاة جلب مقالات تلقائيًا (في النسخة الحقيقية بنستخدم سكريبت خارجي)
document.addEventListener("DOMContentLoaded", function () {
    const articles = [
        {
            title: "📌 الذكاء الاصطناعي يحلل الانتخابات الأمريكية",
            summary: "يتوقع الذكاء الاصطناعي أن تركز الحملة القادمة على الاقتصاد أكثر من أي وقت مضى..."
        },
        {
            title: "💼 الاقتصاد العالمي يبدأ في التعافي",
            summary: "تشير المؤشرات إلى تحسن في الأسواق الأوروبية والآسيوية بدعم من الابتكار التكنولوجي..."
        },
        {
            title: "🤖 الذكاء الاصطناعي في التعليم العربي",
            summary: "تزايد استخدام أدوات AI في المدارس والجامعات خاصةً بعد نجاح التجارب الرقمية خلال الجائحة..."
        }
    ];

    const container = document.getElementById("articles");
    container.innerHTML = "";
    articles.forEach(a => {
        container.innerHTML += `
            <article>
                <h3>${a.title}</h3>
                <p>${a.summary}</p>
            </article>
        `;
    });
});
