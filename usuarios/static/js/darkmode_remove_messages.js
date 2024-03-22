const darkmode = document.getElementById("darkmode");
darkmode.addEventListener("change", () => {
  document.body.classList.toggle("dark");
});

// Method to remove the alert div
const closeButton = document.querySelector("[data-dismiss-target]");
const alertDiv = document.getElementById("alert-3");
const alertDiv2 = document.getElementById("alert-2");
const alertDiv4 = document.getElementById("alert-4");
if (closeButton) {
  closeButton.addEventListener("click", () => {
    if (alertDiv) {
      alertDiv.remove();
    }
    if (alertDiv2) {
      alertDiv2.remove();
    }
    if (alertDiv4) {
      alertDiv4.remove();
    }
  });
}
