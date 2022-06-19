const shiftenInit = function () {
  const buttons = document.getElementsByClassName("edit-button");
  const popup = document.getElementById("shiften-settings-popup");
  const close = document.getElementById("shiften-settings-close");
  close.onclick = () => popup.close();
  [...buttons].forEach((button) => {
    button.onclick = () => {
      console.log(button.value);
      popup.showModal();
    };
  });
};
addLoadEvent(shiftenInit);
