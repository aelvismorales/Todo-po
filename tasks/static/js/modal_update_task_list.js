// Desc: Modal to update a task list
import {
  open_modal,
  close_modal,
  show_message,
} from "./modal_create_task_list.js";

// Constants
const SUCCESS = "success";
const ERROR = "error";

let id_task_list;
function open_update_modal(id) {
  id_task_list = id;
  open_modal(modal_update_task_list);
  populate_update_form(id_task_list);
}

function populate_update_form(id_task_list) {
  // Get the actual task list to update
  const actual_task_list = document.getElementById(
    `task_list_item_${id_task_list}`
  );
  // Get form to update
  const form = document.getElementById("form_update_task_list");

  if (actual_task_list && form) {
    // Complete form with actual task list data
    const name = actual_task_list.getAttribute("data-name");
    const description = actual_task_list.getAttribute("data-description");

    // Set form data to be visible to the user
    form.action = `/tasks/update_task_list/${id_task_list}/`;
    form.name.value = name;
    form.description.value = description;
  }
}

function update_task_list_ui(data, id_task_list) {
  // Get actual task list
  const actual_task_list = document.getElementById(
    `task_list_item_${id_task_list}`
  );
  const name_article = document.getElementById(
    `h_article_task_${id_task_list}`
  );
  const description_article = document.getElementById(
    `description_task_${id_task_list}`
  );

  // Update task list in the UI
  actual_task_list.setAttribute("data-name", data.task_list.name);
  actual_task_list.setAttribute("data-description", data.task_list.description);
  name_article.textContent = data.task_list.name;
  description_article.textContent = data.task_list.description;
}

// Get buttons to open update modal task list
// May an error occur if the button is not found
const btn_update_task_list = document.querySelectorAll("#btn_update_task_list");
const modal_update_task_list = document.getElementById(
  "modal_update_task_list"
);

btn_update_task_list.forEach((btn) => {
  const id = btn.getAttribute("data-id");
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    open_update_modal(id);
  });
});

// Send form data using fetch and async/await
const update_save_button = document.getElementById("update_save_button");
update_save_button.addEventListener("click", async (e) => {
  // Getting form data
  const form = document.getElementById("form_update_task_list");
  const formData = new FormData(form);
  const message_loader_form = document.getElementById(
    "message_loader_update_modal"
  );
  const message_loader = document.getElementById("message_loader");
  // Prevent default form submit
  e.preventDefault();
  // Disable button to avoid multiple clicks
  update_save_button.disabled = true;

  // Check if the form is not empty
  if (formData.get("name") === "" || formData.get("description") === "") {
    show_message(message_loader_form, "Fields cannot be empty", "error");
    update_save_button.disabled = false;
    return;
  }

  // Fetch form data using async/await
  try {
    const response = await fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": "{{csrf_token}}",
      },
    });
    const data = await response.json();

    if (data.status === "success") {
      // Update task list in the UI
      update_task_list_ui(data, id_task_list);
      // Close modal
      close_modal(modal_update_task_list);
      // Show message
      show_message(message_loader, "Task list updated successfully", SUCCESS);
    } else {
      show_message(message_loader_form, "An error occurred", ERROR);
    }
  } catch (error) {
    show_message(message_loader_form, `An error occurred ${error}`, ERROR);
  }
  update_save_button.disabled = false;
});

// Button to close modal update task list
const modal_close_update_svg = document.getElementById(
  "modal_close_update_svg"
);
const modal_close_update_footer_btn = document.getElementById(
  "modal_close_update_footer_btn"
);

// Add event listener to close modal update task list
modal_update_task_list.addEventListener("click", (e) => {
  if (
    e.target === modal_update_task_list ||
    e.target === modal_close_update_svg ||
    e.target === modal_close_update_footer_btn
  ) {
    close_modal(modal_update_task_list);
  }
});
