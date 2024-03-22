import {
  open_modal,
  close_modal,
  show_message,
} from "./modal_create_task_list.js";
let id_task_list;
function remove_task_list_ui(id) {
  const task_list = document.getElementById(`task_list_item_${id}`);
  if (task_list) {
    task_list.remove();
  }
}

// Constants
const SUCCESS = "success";
const ERROR = "error";

// Get buttons to open delete modal task list

const btn_delete_task_list = document.querySelectorAll("#btn_delete_task_list");

const modal_delete_task_list = document.getElementById(
  "modal_delete_task_list"
);

// Get button to confirm delete task list
const delete_save_task_list_button = document.getElementById(
  "delete_save_task_list_button"
);

// Open modal delete task list
btn_delete_task_list.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    id_task_list = btn.getAttribute("data-id");
    open_modal(modal_delete_task_list);
  });
});

delete_save_task_list_button.addEventListener("click", async (e) => {
  const csrftoken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken"))
    .split("=")[1];
  // Disable button to avoid multiple clicks
  delete_save_task_list_button.disabled = true;
  // false flag to show message on the reload page
  localStorage.setItem("show_message", false);

  // Message loader delete modal
  const message_loader_delete = document.getElementById(
    "message_loader_delete_modal"
  );

  //Message loader
  const message_loader = document.getElementById("message_loader");
  try {
    const response = await fetch(`/tasks/delete_task_list/${id_task_list}/`, {
      method: "DELETE",
      body: JSON.stringify({ id: id_task_list }),
      headers: {
        "X-CSRFToken": csrftoken,
      },
    });

    const data = await response.json();
    if (data.status === "success") {
      // reload the page
      localStorage.setItem("show_message", true);
      window.location.reload();
    }
    // Removing the task list from the UI
    // Close modal
    close_modal(modal_delete_task_list);
    // Show message
    show_message(message_loader, "Task list deleted successfully", SUCCESS);
    // Remove task list from the UI
    remove_task_list_ui(id_task_list);
    delete_save_task_list_button.disabled = false;
  } catch (error) {
    show_message(message_loader_delete, `An error occurred ${error}`, ERROR);
    delete_save_task_list_button.disabled = false;
  }
});

// Get buttons to close delete modal task list

const modal_close_delete_svg = document.getElementById(
  "modal_close_delete_svg"
);
const modal_close_delete_footer_btn = document.getElementById(
  "modal_close_delete_footer_btn"
);

// Close modal delete task list
modal_delete_task_list.addEventListener("click", (e) => {
  if (
    e.target === modal_delete_task_list ||
    e.target === modal_close_delete_svg ||
    e.target === modal_close_delete_footer_btn
  ) {
    close_modal(modal_delete_task_list);
  }

  // Showing message if the page is reload
  document.addEventListener("DOMContentLoaded", () => {
    const show_message = localStorage.getItem("show_message");
    if (show_message === "true") {
      const message_loader = document.getElementById("message_loader");
      show_message(message_loader, "Task list deleted successfully", SUCCESS);
      localStorage.setItem("show_message", false);
    }
  });
});
