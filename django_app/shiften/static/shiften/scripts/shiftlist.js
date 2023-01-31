function disableName() {
  const nameInput = document.getElementById("name");
  const selector = document.getElementById("type");
  setTimeout(() => {
    if (selector.value == "event") {
      nameInput.disabled = false;
      nameInput.style.textDecoration = "";
    } else {
      nameInput.disabled = true;
      nameInput.style.textDecoration = "line-through";
    }
  }, 1);
}
// Deze functie werkt alleen maar als model.js ook geladen is
function toggleModalById(modelId) {
  const modal = document.getElementById(modelId);
  typeof modal != "undefined" && modal != null && isModalOpen(modal)
    ? closeModal(modal)
    : openModal(modal);
}
