const disableName = (event) => {
  const nameInput = document.getElementById("name");
  if (event.currentTarget.value == "event") {
    nameInput.disabled = false;
    nameInput.style.textDecoration = "";
  } else {
    nameInput.disabled = true;
    nameInput.style.textDecoration = "line-through";
  }
};

// Deze functie werkt alleen maar als model.js ook geladen is
function toggleModalById(modelId) {
  const modal = document.getElementById(modelId);
  typeof modal != "undefined" && modal != null && isModalOpen(modal)
    ? closeModal(modal)
    : openModal(modal);
  setTimeout(() => {
    Unicorn.call("home", "load_shiftlists");
  }, 250);
}
