import { getData } from "/static/scripts/ajaxTools.js";

let shiftlists;
let user;

export async function main() {
  const json = await getData("ajax");
  shiftlists = json.shiftlists;
  user = json.user;
  toHTML();
}

function toHTML() {
  const shiftlist = document.querySelector(".shiftlist-div");
  shiftlist.replaceChildren();
  if (user.perms.shiftlijst_add) {
    const popup = createShiftlistPopupHTML();
    shiftlist.appendChild(popup);
    const add = document.createElement("button");
    add.innerText = gettext("Add Shiftlist");
    add.onclick = () => {
      popup.showModal();
    };
    shiftlist.appendChild(add);
  }

  const list = document.createElement("ul");
  list.classList.add("shiftlist-list");
  shiftlists.forEach((shiftlist) => {
    const li = document.createElement("li");
    li.classList.add("shiftlist");
    const link = document.createElement("a");
    link.href = shiftlist.id;
    link.innerText = `${
      shiftlist.date.charAt(0).toUpperCase() + shiftlist.date.slice(1)
    } | ${shiftlist.type}`;
    li.appendChild(link);
    list.appendChild(li);
  });
  shiftlist.appendChild(list);
}

function createShiftlistPopupHTML() {
  const popup = document.createElement("dialog");
  // bottom buttons
  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  // safe button
  const safe = document.createElement("button");
  safe.innerText = gettext("Safe");
  safe.onclick = () => {
    createShiftlist();
  };
  bottom.appendChild(safe);
  // close button
  const close = document.createElement("button");
  close.innerText = gettext("Close");
  close.onclick = () => {
    popup.close();
  };
  bottom.appendChild(close);
  popup.appendChild(bottom);
  return popup;
}
