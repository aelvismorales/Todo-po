import {
  open_modal,
  close_modal,
  show_message,
} from "./modal_create_task_list.js";

// Global value
let id_task = null;
const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const btn_delete_task = document.querySelectorAll("#btn_delete_task");

const modal_delete_task = document.getElementById("modal_delete_task");
const message_loader = document.getElementById("message_loader");
const message_loader_delete_modal = document.getElementById(
  "message_loader_delete_modal"
);

// Open modal
if (btn_delete_task) {
  btn_delete_task.forEach((btn) => {
    btn.addEventListener("click", () => {
      id_task = btn.getAttribute("data-id");
      open_modal(modal_delete_task);
    });
  });
}
// Get button to delete task
const btn_delete_save = document.getElementById("btn_delete_save");
btn_delete_save.addEventListener("click", async (e) => {
  try {
    const response = await fetch(`/tasks/task_list/task/delete/${id_task}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": csrf_token,
      },
    });

    const data = await response.json();
    if (data.status === "success") {
      close_modal(modal_delete_task);
      document.getElementById(`task-${id_task}`).remove();
      show_message(message_loader, "Task deleted successfully", "success");
    } else {
      show_message(message_loader_delete_modal, "Error deleting task", "error");
    }
  } catch (error) {
    show_message(
      message_loader_delete_modal,
      `Error deleting task ${error}`,
      "error"
    );
  }
});

// Close modal
const modal_delete_close_svg = document.getElementById(
  "modal_delete_close_svg"
);
const modal_delete_close_footer_btn = document.getElementById(
  "modal_delete_close_footer_btn"
);

if (modal_delete_task) {
  modal_delete_task.addEventListener("click", (e) => {
    if (
      e.target === modal_delete_task ||
      e.target === modal_delete_close_svg ||
      e.target === modal_delete_close_footer_btn
    ) {
      close_modal(modal_delete_task);
    }
  });
}
