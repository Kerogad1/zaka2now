fetch('articles/index.json')
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById('articles-container');
    data.forEach(article => {
      const div = document.createElement('div');
      div.className = 'article';
      div.innerHTML = `
        <h2><a href="articles/${article.filename}">${article.title}</a></h2>
        ${article.img_url ? `<img src="${article.img_url}" alt="image">` : ''}
        <p>${article.summary}</p>
      `;
      container.appendChild(div);
    });
  });