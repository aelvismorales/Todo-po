// Desc: Modal to create a task list
// Constants
const SUCCESS = "success";
const ERROR = "error";
//const WARNING = 'warning';
// * Function to open and close modals
export function open_modal(modal) {
  modal.classList.remove("hidden");
  modal.classList.add("block");
  modal.setAttribute("aria-hidden", "false");
}

export function close_modal(modal) {
  modal.classList.remove("block");
  modal.classList.add("hidden");
  modal.setAttribute("aria-hidden", "true");
}

export function show_message(message_loader, message, type) {
  let div;
  if (type === SUCCESS) {
    div = create_div_alert(
      "alert-3",
      "flex items-center p-4 mb-4 text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400",
      message
    );
  } else if (type === ERROR) {
    div = create_div_alert(
      "alert-2",
      "flex items-center p-4 mb-4 text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400",
      message
    );
  } else {
    div = create_div_alert(
      "alert-4",
      "flex items-center p-4 mb-4 text-yellow-800 rounded-lg bg-yellow-50 dark:bg-gray-800 dark:text-yellow-400",
      message
    );
  }
  message_loader.appendChild(div);
  setTimeout(() => {
    message_loader.removeChild(div);
  }, 2000);
}

function create_div_alert(id, className, message) {
  const div = document.createElement("div");
  div.id = id;
  div.className = className;
  div.role = "alert";
  div.innerHTML = `<svg class="flex-shrink-0 w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z" /></svg><span class="sr-only">Info</span><div class="ms-3 text-sm font-medium">${message}</div>`;
  return div;
}

// !* Open modal crear_task_list

// Get button to open modal
const btn_crear_task_list = document.getElementById("btn_crear_task_list");

// Get modal
const modal_crear_task_list = document.getElementById("modal_crear_task_list");

// Get close buttons
const modal_close_svg = document.getElementById("modal_close_svg");
const modal_close_footer_btn = document.getElementById(
  "modal_close_footer_btn"
);

// Open modal
if (btn_crear_task_list) {
  btn_crear_task_list.addEventListener("click", (e) => {
    e.stopPropagation();
    open_modal(modal_crear_task_list);
  });
}

// Close modal
if (modal_crear_task_list) {
  modal_crear_task_list.addEventListener("click", (e) => {
    if (
      e.target === modal_crear_task_list ||
      e.target === modal_close_svg ||
      e.target === modal_close_footer_btn
    ) {
      close_modal(modal_crear_task_list);
    }
  });
}
// Send form data using fetch
const save_button = document.getElementById("save_button");

if (save_button) {
  save_button.addEventListener("click", async (e) => {
    // Getting form data
    const form = document.getElementById("form_crear_task_list");
    const formData = new FormData(form);
    const message_loader_form = document.getElementById(
      "message_loader_crear_modal"
    );
    // Prevent default form submit
    e.preventDefault();
    // Disable button to avoid multiple clicks
    save_button.disabled = true;

    // Check if the form is not empty
    if (formData.get("name") === "" || formData.get("description") === "") {
      show_message(message_loader_form, "Fields cannot be empty", "error");
      save_button.disabled = false;
      return;
    }
    // Save a flag in localStorage to show the message
    localStorage.setItem("show_message", false);

    // Fetch form data using async/await
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": "{{csrftoken}}",
        },
      });
      if (response.ok) {
        show_message(
          message_loader_form,
          "Task list created successfully",
          "sucess"
        );
        close_modal(modal_crear_task_list);
        save_button.disabled = false;
        form.reset();
        localStorage.setItem("show_message", true);
        window.location.reload();
      } else {
        show_message(message_loader_form, "An error occurred", "error");
        save_button.disabled = false;
      }
    } catch (error) {
      show_message(message_loader_form, `An eror occurred ${error}`, "error");
      save_button.disabled = false;
    }
  });
}

// * Check if the message should be shown
document.addEventListener("DOMContentLoaded", () => {
  const show_message_flag = localStorage.getItem("show_message");
  const message_loader = document.getElementById("message_loader");

  if (show_message_flag === "true") {
    show_message(message_loader, "Task list created successfully", SUCCESS);
    localStorage.setItem("show_message", false);
  }
});
