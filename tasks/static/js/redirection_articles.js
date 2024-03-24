const articles = document.querySelectorAll(".task_list_item");
articles.forEach((article) => {
  article.addEventListener("click", (e) => {
    console.log(localStorage.getItem("show_message"));
    const taskListId = e.currentTarget.getAttribute("data-id");
    window.location.href = `/tasks/task_list/${taskListId}`;
  });
});
