document.addEventListener('DOMContentLoaded',()=>{
  fetch('articles/index.json').then(res=>res.json()).then(data=>{
    const list=document.getElementById('article-list');
    const trending=document.getElementById('trending-list');
    list.innerHTML=''; trending.innerHTML='';
    data.articles.forEach((a,i)=>{
      const card=document.createElement('div'); card.className='article-card';
      card.innerHTML=`<h3>${a.title}</h3><p>${a.summary}</p><a href="articles/${a.filename}">Read more</a>`;
      list.appendChild(card);
      if(i<3) trending.appendChild(card.cloneNode(true));
    });
  });
  // Search
  document.getElementById('search-input').addEventListener('input',e=>{
    const q=e.target.value.toLowerCase();
    fetch('articles/index.json').then(res=>res.json()).then(data=>{
      const results=document.getElementById('search-results');
      results.innerHTML='';
      data.articles.filter(a=>a.title.toLowerCase().includes(q)).forEach(a=>{
        const d=document.createElement('div'); d.className='article-card';
        d.innerHTML=`<h3>${a.title}</h3><p>${a.summary}</p><a href="articles/${a.filename}">Read more</a>`;
        results.appendChild(d);
      });
    });
  });
});