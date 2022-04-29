const switchColor = function () {
  colormode = localStorage.getItem("colormode");
  if (colormode !== "dark") enableDarkMode();
  else enableLightMode();
};

const enableDarkMode = () => {
  document.body.classList.add("darkmode");
  localStorage.setItem("colormode", "dark");
};
const enableLightMode = () => {
  document.body.classList.remove("darkmode");
  localStorage.setItem("colormode", "light");
};

let colormode = localStorage.getItem("colormode");
if (colormode === "dark") {
  enableDarkMode();
}

const init = function () {
  const darkModeToggle = document.getElementById("color-mode-btn");
  if (darkModeToggle !== null)
    darkModeToggle.addEventListener("click", switchColor);
};

window.onload = init;
