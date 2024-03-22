const articles = document.querySelectorAll(".task_list_item");
console.log(articles);
articles.forEach((article) => {
  article.addEventListener("click", (e) => {
    const taskListId = e.currentTarget.getAttribute("data-id");
    window.location.href = `/tasks/task_list/${taskListId}`;
  });
});
