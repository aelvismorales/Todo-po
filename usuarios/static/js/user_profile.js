let badgeList = document.getElementById("badgeList");
document.getElementById("scrollRight").addEventListener("click", function () {
  badgeList.scrollBy({
    left: 64, // Adjust scroll distance as needed
    behavior: "smooth", // Optional: Smooth scrolling animation
  });
});

document.getElementById("scrollLeft").addEventListener("click", function () {
  badgeList.scrollBy({
    left: -64, // Adjust scroll distance as needed
    behavior: "smooth", // Optional: Smooth scrolling animation
  });
});

// Load sidebar user content
const userContent = document.getElementById("userContent");
const sidebarUser = document.getElementById("sidebarUser");

// Verifica si hay un valor en el localStorage para el estado del toggle
const toggleState = localStorage.getItem("sidebarToggleState");
if (toggleState === "false") {
  userContent.classList.remove("flex");
  userContent.classList.add("hidden");
  userContent.setAttribute("aria-hidden", "false");
} else {
  userContent.classList.remove("hidden");
  userContent.classList.add("flex");
  userContent.setAttribute("aria-hidden", "true");
}

sidebarUser.addEventListener("click", function () {
  sidebarUser.dataset.toggle =
    sidebarUser.dataset.toggle === "true" ? "false" : "true";
  if (sidebarUser.dataset.toggle === "false") {
    userContent.classList.remove("flex");
    userContent.classList.add("hidden");
    userContent.setAttribute("aria-hidden", "false");
  } else {
    userContent.classList.remove("hidden");
    userContent.classList.add("flex");
    userContent.setAttribute("aria-hidden", "true");
  }

  // Guarda el estado del toggle en el localStorage
  localStorage.setItem("sidebarToggleState", sidebarUser.dataset.toggle);
});
