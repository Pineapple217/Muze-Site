function disableName() {
  const nameInput = document.getElementById("id_name");
  const selector = document.getElementById("id_type");
  setTimeout(() => {
    if (selector.value == "month") {
      nameInput.disabled = true;
      nameInput.style.textDecoration = "line-through";
    } else {
      nameInput.disabled = false;
      nameInput.style.textDecoration = "";
    }
  }, 1);
}
document.getElementById("id_type").onchange = disableName;

// Deze functie werkt alleen maar als model.js ook geladen is
function toggleModalById(modelId) {
  const modal = document.getElementById(modelId);
  typeof modal != "undefined" && modal != null && isModalOpen(modal)
    ? closeModal(modal)
    : openModal(modal);
}
