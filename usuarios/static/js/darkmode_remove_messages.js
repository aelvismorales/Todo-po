// Dark mode toggle function
function toggleDarkMode() {
  const darkModeCheckbox = document.getElementById("darkmode");
  if (darkModeCheckbox) {
    if (darkModeCheckbox.checked) {
      // Dark mode enabled
      document.documentElement.classList.toggle("dark");
    } else {
      // Light mode enabled
      document.documentElement.classList.remove("dark");
    }

    // Guarda el estado del modo oscuro en el localStorage
    localStorage.setItem("darkModeState", darkModeCheckbox.checked);
  }
}

// Inicializa el modo oscuro según la preferencia del usuario almacenada en localStorage
if (localStorage.getItem("darkModeState") === "true") {
  document.documentElement.classList.toggle("dark");
  document.getElementById("darkmode").checked = true;
}

// Dark mode button event listener
document.getElementById("darkmode").addEventListener("change", function () {
  toggleDarkMode();
});

/*function removeMessages() {
  // Method to remove the alert div
  const alertDiv = document.getElementById("alert-3");
  const alertDiv2 = document.getElementById("alert-2");
  const alertDiv4 = document.getElementById("alert-4");

  // Method to remove the alert div after 5 seconds
  if (alertDiv) {
    setTimeout(() => {
      alertDiv.remove();
    }, 2500);
  }
  if (alertDiv2) {
    setTimeout(() => {
      alertDiv2.remove();
    }, 2500);
  }
  if (alertDiv4) {
    setTimeout(() => {
      alertDiv4.remove();
    }, 2500);
  }
}

// Call the removeMessages function
removeMessages();*/
