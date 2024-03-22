import {
  open_modal,
  close_modal,
  show_message,
} from "./modal_create_task_list.js";

let id_task_list;

// Constants
const SUCCESS = "success";
const ERROR = "error";

// Get buttons to open modal add task to task list
const btn_add_task_to_task_list = document.querySelectorAll(
  "#btn_add_task_to_task_list"
);
const modal_add_task_to_task_list = document.getElementById(
  "modal_add_task_to_task_list"
);

btn_add_task_to_task_list.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    id_task_list = btn.getAttribute("data-id");
    open_modal(modal_add_task_to_task_list);
  });
});

// Get button to save task to task list
const save_task_to_task_list_button = document.getElementById(
  "save_task_to_task_list_button"
);

// Save task to task list
save_task_to_task_list_button.addEventListener("click", async (e) => {
  e.preventDefault();
  // Getting csrftoken
  const csrftoken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken"))
    .split("=")[1];
  // Getting form data
  const form = document.getElementById("form_add_task_to_task_list");
  const formData = new FormData(form);
  if (form) {
    form.action = `/tasks/add_task_to_task_list/${id_task_list}/`;
  }
  // Getting message loader form
  const message_loader_form = document.getElementById(
    "message_loader_form_add_task_to_task_list"
  );

  // Flag to show message after reload
  localStorage.setItem("show_message", false);

  // Prevent multiple clicks
  save_task_to_task_list_button.disabled = true;
  // Check if the form is not empty
  if (formData.get("name") === "" || formData.get("description") === "") {
    show_message(message_loader_form, "Fields cannot be empty", "error");
    save_task_to_task_list_button.disabled = false;
    return;
  }

  // Fetch form data using async/await
  try {
    const response = await fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrftoken,
      },
    });
    const data = await response.json();
    if (response.ok) {
      close_modal(modal_add_task_to_task_list);
      localStorage.setItem("show_message", true);
      location.reload();
    } else {
      show_message(message_loader_form, data.message, ERROR);
      save_task_to_task_list_button.disabled = false;
    }
  } catch (error) {
    show_message(message_loader_form, "Server error", ERROR);
    save_task_to_task_list_button.disabled = false;
  }
});

//Get button to close modal
const close_modal_add_task_to_task_list_svg = document.getElementById(
  "close_modal_add_task_to_task_list_svg"
);
const close_modal_add_task_to_task_list_footer_btn = document.getElementById(
  "close_modal_add_task_to_task_list_footer_btn"
);

// Close modal
modal_add_task_to_task_list.addEventListener("click", (e) => {
  if (
    e.target === modal_add_task_to_task_list ||
    e.target === close_modal_add_task_to_task_list_svg ||
    e.target === close_modal_add_task_to_task_list_footer_btn
  ) {
    close_modal(modal_add_task_to_task_list);
  }
});

// Showing message after reload
document.addEventListener("DOMContentLoaded", () => {
  const show_message_flag = localStorage.getItem("show_message");
  if (show_message_flag === "true") {
    const message_loader = document.getElementById("message_loader");
    show_message(message_loader, "Task added successfully", SUCCESS);
    localStorage.setItem("show_message", false);
  }
});
