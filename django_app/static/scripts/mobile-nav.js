// Mobile menu

const menuTrigger = document.querySelector(".mobile");
const menu = document.querySelector(".desktop");
const mobileQuery = getComputedStyle(document.body).getPropertyValue(
  "--phoneWidth"
);
const isMobile = () => window.matchMedia(mobileQuery).matches;
const isMobileMenu = () => {
  menuTrigger && menuTrigger.classList.toggle("hidden", !isMobile());
  menu && menu.classList.toggle("hidden", isMobile());
};

isMobileMenu();

// menuTrigger &&
//   menuTrigger.addEventListener(
//     "click",
//     () => menu && menu.classList.toggle("hidden")
//   );

window.addEventListener("resize", isMobileMenu);

const burger = document.getElementById("burger");
const burgerlist = document.getElementById("burger-list");

burger.addEventListener("click", () => {
  burgerlist.classList.toggle("hidden");
});
