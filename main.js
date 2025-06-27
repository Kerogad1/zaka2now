document.addEventListener("DOMContentLoaded", () => {
  fetch('articles/index.json')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById("articles-container");
      data.forEach(article => {
        const div = document.createElement("div");
        div.innerHTML = `<h2><a href="${article.link}">${article.title}</a></h2><p>${article.summary}</p>`;
        container.appendChild(div);
      });
    });
});
