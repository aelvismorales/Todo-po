import {
  open_modal,
  close_modal,
  show_message,
} from "./modal_create_task_list.js";

// Get button to open modal
const btn_crear_task = document.getElementById("btn_crear_task");
const modal_crear_task = document.getElementById("modal_crear_task");
// Open modal
btn_crear_task.addEventListener("click", () => {
  open_modal(modal_crear_task);
});

// Get button to save task
const btn_create_save = document.getElementById("btn_create_save");
// Save task
if (btn_create_save) {
  btn_create_save.addEventListener("click", () => {
    const id_task_list =
      document.getElementById("tasks-container").dataset.tlid;
    const form = document.getElementById("form_create_task");
    const formData = new FormData(form);
    const url = "/tasks/add_task_to_task_list/" + id_task_list + "/";
    const csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0]
      .value;

    const message_loader_create_modal = document.getElementById(
      "message_loader_create_modal"
    );

    // Flag to show message when page is reloaded
    localStorage.setItem("show_message", false);

    try {
      const response = fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrftoken,
        },
      });
      if (response.ok) {
        close_modal(modal_crear_task);
        localStorage.setItem("show_message", true);
        location.reload();
      } else {
        show_message(
          message_loader_create_modal,
          "Error creating task",
          "error"
        );
      }
    } catch (error) {
      show_message(
        message_loader_create_modal,
        `Error creating task ${error}`,
        "error"
      );
    }
  });
}

// Close modal
const btn_create_close_svg = document.getElementById("btn_create_close_svg");
const btn_create_footer_close = document.getElementById(
  "btn_create_footer_close"
);

modal_crear_task.addEventListener("click", (e) => {
  if (
    e.target === modal_crear_task ||
    e.target === btn_create_close_svg ||
    e.target === btn_create_footer_close
  ) {
    close_modal(modal_crear_task);
  }
});

// Show message when page is reloaded
/*document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed");
  const show_message_flag = localStorage.getItem("show_message");
  const message_loader = document.getElementById("message_loader");
  console.log(show_message_flag);
  if (show_message_flag) {
    show_message(message_loader, "Task created successfully", "success");
    localStorage.removeItem("show_message");
  }
});
*/
