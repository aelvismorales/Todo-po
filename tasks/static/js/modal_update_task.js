import {
  open_modal,
  close_modal,
  show_message,
} from "./modal_create_task_list.js";
async function populate_update_form(id) {
  try {
    const response = await fetch(`/tasks/task_list/task/update/${id}/`, {
      method: "GET",
      headers: {
        "X-CSRFToken": csrftoken,
      },
    });
    const task = await response.json();
    const form = document.getElementById("update_task_form");
    form.elements["title"].value = task.task.title;
    form.elements["description"].value = task.task.description;
    form.elements["completed"].checked = task.task.completed;
    open_modal(modal_update_task);
  } catch (error) {
    show_message(message_loader, `Error updating task ${error}`, "error");
  }
}

function update_task_ui(data, id) {
  const task_title = document.getElementById(`h_task_${id}`);
  const task_completed = document.getElementById(`p_task_completed_${id}`);
  const task_description = document.getElementById(`p_task_description_${id}`);
  task_title.textContent = data.title;
  task_description.textContent = data.description;

  if (data.completed) {
    task_completed.checked = data.completed;
    task_completed.innerHTML = `<strong>Completed: </strong>
    <svg class="w-6 h-6 text-green-500" aria-hidden="true"
         xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
        <path fill-rule="evenodd"
              d="M12 2c-.791 0-1.55.314-2.11.874l-.893.893a.985.985 0 0 1-.696.288H7.04A2.984 2.984 0 0 0 4.055 7.04v1.262a.986.986 0 0 1-.288.696l-.893.893a2.984 2.984 0 0 0 0 4.22l.893.893a.985.985 0 0 1 .288.696v1.262a2.984 2.984 0 0 0 2.984 2.984h1.262c.261 0 .512.104.696.288l.893.893a2.984 2.984 0 0 0 4.22 0l.893-.893a.985.985 0 0 1 .696-.288h1.262a2.984 2.984 0 0 0 2.984-2.984V15.7c0-.261.104-.512.288-.696l.893-.893a2.984 2.984 0 0 0 0-4.22l-.893-.893a.985.985 0 0 1-.288-.696V7.04a2.984 2.984 0 0 0-2.984-2.984h-1.262a.985.985 0 0 1-.696-.288l-.893-.893A2.984 2.984 0 0 0 12 2Zm3.683 7.73a1 1 0 1 0-1.414-1.413l-4.253 4.253-1.277-1.277a1 1 0 0 0-1.415 1.414l1.985 1.984a1 1 0 0 0 1.414 0l4.96-4.96Z"
              clip-rule="evenodd" />
    </svg>`;
  } else {
    task_completed.checked = data.completed;
    task_completed.innerHTML = `<strong>Completed: </strong>
    <svg class="w-6 h-6 text-gray-80" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
         viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m8.032 12 1.984 1.984 4.96-4.96m4.55 5.272.893-.893a1.984 1.984 0 0 0 0-2.806l-.893-.893a1.984 1.984 0 0 1-.581-1.403V7.04a1.984 1.984 0 0 0-1.984-1.984h-1.262a1.983 1.983 0 0 1-1.403-.581l-.893-.893a1.984 1.984 0 0 0-2.806 0l-.893.893a1.984 1.984 0 0 1-1.403.581H7.04A1.984 1.984 0 0 0 5.055 7.04v1.262c0 .527-.209 1.031-.581 1.403l-.893.893a1.984 1.984 0 0 0 0 2.806l.893.893c.372.372.581.876.581 1.403v1.262a1.984 1.984 0 0 0 1.984 1.984h1.262c.527 0 1.031.209 1.403.581l.893.893a1.984 1.984 0 0 0 2.806 0l.893-.893a1.985 1.985 0 0 1 1.403-.581h1.262a1.984 1.984 0 0 0 1.984-1.984V15.7c0-.527.209-1.031.581-1.403Z" />
    </svg>`;
  }
}

// Global task_id
let id_task = null;
const csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

const btn_update_task = document.querySelectorAll("#btn_update_task");
const modal_update_task = document.getElementById("modal_update_task");
const message_loader = document.getElementById("message_loader");
const message_loader_update_modal = document.getElementById(
  "message_loader_update_modal"
);

// Open modal
if (btn_update_task) {
  btn_update_task.forEach((btn) => {
    btn.addEventListener("click", () => {
      id_task = btn.getAttribute("data-id");
      populate_update_form(id_task);
    });
  });
}

// Get button to save task
const btn_update_save = document.getElementById("btn_update_save");

// Save Task updated
if (btn_update_save) {
  btn_update_save.addEventListener("click", async (e) => {
    e.preventDefault();
    const form = document.getElementById("update_task_form");
    const formData = new FormData(form);
    const url = `/tasks/task_list/task/update/${id_task}/`;
    //Disable button to avoid multiple clicks
    btn_update_save.disabled = true;

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrftoken,
        },
      });
      const data = await response.json();

      if (data.status === "success") {
        close_modal(modal_update_task);
        update_task_ui(data.task, id_task);
        show_message(message_loader, "Task updated successfully", "success");
        btn_update_save.disabled = false;
      } else {
        show_message(
          message_loader_update_modal,
          "Error updating task",
          "error"
        );
        btn_update_save.disabled = false;
      }
    } catch (error) {
      show_message(
        message_loader_update_modal,
        `Error updating task ${error}`,
        "error"
      );
      btn_update_save.disabled = false;
    }
  });
}

// Get buttons to close modal
const modal_update_close_svg = document.getElementById(
  "modal_update_close_svg"
);
const modal_update_close_footer_btn = document.getElementById(
  "modal_update_close_footer_btn"
);

// Close modal

if (modal_update_task) {
  modal_update_task.addEventListener("click", (e) => {
    if (
      e.target === modal_update_task ||
      e.target === modal_update_close_svg ||
      e.target === modal_update_close_footer_btn
    ) {
      close_modal(modal_update_task);
    }
  });
}
