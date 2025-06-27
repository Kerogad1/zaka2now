fetch('articles/index.json')
  .then(res=>res.json())
  .then(data=>{
    const c=document.getElementById('articles-container'); c.innerHTML='';
    data.articles.forEach(a=>{
      const d=document.createElement('div');
      d.innerHTML=`<h2><a href="articles/${a.filename}">${a.title}</a></h2><p>${a.summary}</p>`;
      c.appendChild(d);
    });
});