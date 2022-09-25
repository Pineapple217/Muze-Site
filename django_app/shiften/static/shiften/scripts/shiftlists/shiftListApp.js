import { getData } from "/static/scripts/ajaxTools.js";
import { creatShiftlistrequest } from "./toServer.js";

let shiftlists;
let user;
let types;
let templates;

export async function main() {
  try {
    const json = await getData("ajax");
    shiftlists = json.shiftlists;
    user = json.user;
    types = json.types;
    templates = json.templates;
    toHTML();
  } catch (error) {
    alert(error);
  }
}

function toHTML() {
  const shiftlist = document.querySelector(".shiftlist-div");
  shiftlist.replaceChildren();
  const h1 = document.createElement("h1");
  h1.innerText = gettext("Shiftlists");
  const header = document.createElement("div");
  header.classList.add("header");
  header.appendChild(h1);
  const buttons = document.createElement("div");
  buttons.classList.add("top-buttons");
  if (user.perms.shiftlijst_add) {
    const popup = createShiftlistPopupHTML();
    shiftlist.appendChild(popup);
    const add = document.createElement("button");
    add.innerText = gettext("Add Shiftlist");
    add.onclick = () => {
      popup.showModal();
    };
    header.appendChild(add);

    const popupTemplate = createShiftlistTemplatePopup();
    shiftlist.appendChild(popupTemplate);
    const addTemplate = document.createElement("button");
    addTemplate.innerText = gettext("Add Shiftlist with template");
    addTemplate.onclick = () => {
      popupTemplate.showModal();
    };
    header.appendChild(addTemplate);
  }
  if (user.perms.template_view) {
    const templates = document.createElement("button");
    templates.innerText = gettext("Templates");
    templates.classList.add("title-btns");
    templates.onclick = () => {
      window.location.href = "templates";
    };
    header.appendChild(templates);
  }
  // header.appendChild(buttons);
  shiftlist.appendChild(header);
  const list = document.createElement("ul");
  list.classList.add("shiftlist-list");
  shiftlists.sort((a, b) => {
    if (a.date > b.date) return 1;
    if (a.date < b.date) return -1;
    return 0;
  });
  shiftlists.forEach((shiftlist) => {
    const li = document.createElement("li");
    li.classList.add("shiftlist");
    if (!shiftlist.is_active) {
      li.classList.add("red");
    }
    const link = document.createElement("a");
    link.href = shiftlist.id;
    const listName = shiftlist.string;
    link.innerText = `${
      listName.charAt(0).toUpperCase() + listName.slice(1)
    } | ${shiftlist.type}`;
    li.appendChild(link);
    list.appendChild(li);
  });
  shiftlist.appendChild(list);
}

function createShiftlistPopupHTML() {
  const popup = document.createElement("dialog");
  popup.classList.add("create-shiftlist-popup");

  const h1 = document.createElement("h1");
  h1.innerText = gettext("Create Shiftlist");
  popup.appendChild(h1);

  const options = document.createElement("div");
  options.classList.add("options");

  const name = document.createElement("input");
  const nameLbl = document.createElement("label");
  name.id = "name";
  name.type = "text";
  name.maxLength = 300;
  name.classList.add("hidden");
  nameLbl.classList.add("hidden");
  nameLbl.htmlFor = "name";
  nameLbl.innerText = gettext("Name");
  options.appendChild(nameLbl);
  options.appendChild(name);

  const date = document.createElement("input");
  const dateLbl = document.createElement("label");
  date.id = "date";
  date.type = "date";
  dateLbl.htmlFor = "date";
  dateLbl.innerText = gettext("Date");
  options.appendChild(dateLbl);
  options.appendChild(date);

  const typeLbl = document.createElement("label");
  const type = document.createElement("select");
  type.id = "type";
  typeLbl.htmlFor = "type";
  typeLbl.innerText = gettext("Type");
  types.forEach((t) => {
    const option = document.createElement("option");
    option.innerText = t[1];
    option.value = t[0];
    type.appendChild(option);
  });
  type.onchange = () => {
    const selected = type.options[type.selectedIndex].value;
    if (selected == "month") {
      name.classList.add("hidden");
      nameLbl.classList.add("hidden");
      name.value = "";
    } else {
      name.classList.remove("hidden");
      nameLbl.classList.remove("hidden");
    }
  };
  options.appendChild(typeLbl);
  options.appendChild(type);

  popup.appendChild(options);

  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  const safe = document.createElement("button");
  safe.innerText = gettext("Save");
  safe.onclick = () => {
    if (date.value) createShiftlist(name.value, date.value, type.value);
  };
  bottom.appendChild(safe);
  const close = document.createElement("button");
  close.innerText = gettext("Close");
  close.onclick = () => {
    popup.close();
  };
  bottom.appendChild(close);
  popup.appendChild(bottom);

  return popup;
}

function createShiftlistTemplatePopup() {
  const popup = document.createElement("dialog");
  popup.classList.add("create-shiftlist-template-popup");

  const h1 = document.createElement("h1");
  h1.innerText = gettext("Create Shiftlist with template");
  popup.appendChild(h1);

  const options = document.createElement("div");
  options.classList.add("options");

  const templateLbl = document.createElement("label");
  const template = document.createElement("select");
  template.id = "template";
  templateLbl.htmlFor = "template";
  templateLbl.innerText = gettext("Template");
  templates.forEach((t) => {
    const option = document.createElement("option");
    option.innerText = t.name;
    option.value = t.id;
    template.appendChild(option);
  });
  options.appendChild(templateLbl);
  options.appendChild(template);

  const date = document.createElement("input");
  const dateLbl = document.createElement("label");
  date.id = "date";
  date.type = "date";
  dateLbl.htmlFor = "date";
  dateLbl.innerText = gettext("Date");
  options.appendChild(dateLbl);
  options.appendChild(date);

  popup.appendChild(options);

  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  const safe = document.createElement("button");
  safe.innerText = gettext("Save");
  safe.onclick = () => {
    if (date.value) createShiftlistTemplate(template.value, date.value);
  };
  bottom.appendChild(safe);
  const close = document.createElement("button");
  close.innerText = gettext("Close");
  close.onclick = () => {
    popup.close();
  };
  bottom.appendChild(close);
  popup.appendChild(bottom);
  return popup;
}

async function createShiftlist(name, date, type) {
  const info = {
    name: name,
    date: date,
    type: type,
  };
  const response = await creatShiftlistrequest(info, "create_shiftlist");
  if (response.body.status == "succes") {
    shiftlists.push({
      date: date,
      type: response.body.shiftlist_info.type,
      name: name,
      id: response.body.shiftlist_info.id,
      string: response.body.shiftlist_info.string,
    });
    toHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function createShiftlistTemplate(id, templateVar) {
  const info = {
    id: id,
    vars: templateVar,
  };
  const response = await creatShiftlistrequest(
    info,
    "create_shiftlist_template"
  );
  if (response.body.status == "succes") {
    shiftlists.push({
      date: response.body.shiftlist_info.date,
      type: response.body.shiftlist_info.type,
      name: response.body.shiftlist_info.name,
      id: response.body.shiftlist_info.id,
      string: response.body.shiftlist_info.string,
    });
    toHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}
