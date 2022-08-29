import {
  request,
  manageShiftRequest,
  createShiftRequest,
  manageShiftlistRequest,
} from "./toServer.js";
import { getData } from "/static/scripts/ajaxTools.js";

let list;
let user;
let shifts;
let leden;
let types;
let available;

let firstLoad = false;
export async function main() {
  try {
    const json = await getData("/ajax");
    list = json.list;
    user = json.user;
    shifts = json.shifts;
    leden = json.leden;
    types = json.types;
    available = json.available;
    shiftsToHTML();
  } catch (error) {
    const body = document.querySelector(".content");
    const h1 = document.createElement("h1");
    h1.innerText = error.message;
    body.appendChild(h1);
  }
}

function sortShifts() {
  shifts = shifts.sort((a, b) => {
    const aD = a.date.replace("-", "") + a.start.replace(":", "");
    const bD = b.date.replace("-", "") + b.start.replace(":", "");
    if (aD > bD) return 1;
    if (aD < bD) return -1;
  });
}

function shiftsToHTML() {
  const header = document.querySelector(".main-header");
  const h1 = document.createElement("h1");
  const shiftList = document.getElementById("shiftlist");
  shiftList.replaceChildren();
  header.replaceChildren();
  h1.innerText = gettext(
    `${list.string.charAt(0).toUpperCase() + list.string.slice(1)}`
  );
  header.appendChild(h1);
  let shiftdate = "";
  let day;
  shifts.forEach((shift) => {
    if (shiftdate != shift.date) {
      const h3 = document.createElement("h2");
      h3.innerText = `${shift.string}`;
      shiftList.appendChild(h3);
      day = document.createElement("div");
      day.classList.add("day");
    }
    const shiftDiv = document.createElement("div");
    shiftDiv.classList.add("shift");
    shiftDiv.classList.add("anchor");
    shiftDiv.id = shift.id;
    const h4 = document.createElement("h3");
    h4.innerText = `${shift.start} - ${shift.end}`;
    if (user.perms.shift_change) {
      //Can EDIT
      h4.innerText += " ";
      const edit = document.createElement("span");
      edit.classList.add("edit-button");
      edit.value = shift.id;
      edit.onclick = () => {
        showEditPopup(shift);
      };
      h4.appendChild(edit);
    }
    shiftDiv.appendChild(h4);
    if (shift.info) {
      const info = document.createElement("p");
      info.classList.add("extra-info");
      info.innerText = shift.info;
      shiftDiv.appendChild(info);
    }
    const ul = document.createElement("ul");
    ul.classList.add("shifters");
    // shift.shifters.forEach((s) => {
    //   let li = document.createElement("li");
    //   li.innerText = s.name;
    //   if (s.id == user.id) li.classList.add("loggedshifter");
    //   ul.appendChild(li);
    // });
    for (let i = 0; i < shift.max; i++) {
      const li = document.createElement("li");
      if (shift.shifters[i]) {
        li.innerText = shift.shifters[i].name;
      } else {
        li.classList.add("empty");
      }
      ul.appendChild(li);
    }
    shiftDiv.appendChild(ul);
    const buttonDiv = document.createElement("div");
    buttonDiv.classList.add("shift-button-status");
    if (shift.shifters.map((s) => s.id).includes(user.id)) {
      // Clearshift
      const button = document.createElement("button");
      button.value = shift.id;
      button.innerText = gettext("Clear shift");
      button.onclick = () => {
        clearShift(shift);
      };
      buttonDiv.appendChild(button);
    } else if (shift.max <= shift.shifters.length) {
      // Shift FULL
      // const vol = document.createElement("p");
      // vol.classList.add("volle-shift");
      // vol.innerText = gettext("Shift Full");
      // buttonDiv.appendChild(vol);
    } else {
      // Take shift
      const button = document.createElement("button");
      button.value = shift.id;
      button.innerText = gettext("Take shift");
      button.onclick = () => {
        takeShift(shift);
      };
      buttonDiv.appendChild(button);
    }
    shiftDiv.appendChild(buttonDiv);
    day.appendChild(shiftDiv);
    if (shiftdate != shift.date) {
      shiftdate = shift.date;
      shiftList.appendChild(day);
    }
  });
  if (user.perms.shift_change) {
    const popup = document.createElement("dialog");
    popup.classList.add("shift-edit-popup");
    shiftList.appendChild(popup);
  }
  if (user.perms.shiftlist_edit) {
    const edit = document.createElement("button");
    edit.innerText = gettext("Edit");
    edit.classList.add("title-btns");
    edit.onclick = () => {
      const listEditPopup = createListEditPopup();
      shiftList.appendChild(listEditPopup);
      listEditPopup.showModal();
    };
    header.appendChild(edit);
  }
  if (user.perms.shift_add) {
    const add = document.createElement("button");
    add.innerText = gettext("Add shift");
    add.classList.add("title-btns");
    add.onclick = () => {
      showCreatePopup();
    };
    header.appendChild(add);
    const popup = document.createElement("dialog");
    popup.classList.add("shift-create-popup");
    shiftList.appendChild(popup);
  }
  if (user.perms.available_view) {
    const div = document.createElement("div");
    div.classList.add("available-slideout");
    const head = document.createElement("h1");
    head.innerText = gettext("Not available");
    div.appendChild(head);
    available.forEach((avail) => {
      const availDiv = document.createElement("div");
      const lid = document.createElement("h2");
      lid.innerText = avail.lid;
      availDiv.appendChild(lid);
      const date = document.createElement("p");
      date.innerText = avail.date;
      availDiv.appendChild(date);
      if (avail.info) {
        const info = document.createElement("p");
        info.innerText = avail.info;
        availDiv.appendChild(info);
      }
      div.appendChild(availDiv);
    });
    console.log(available);

    shiftList.appendChild(div);
    const slideoutBtn = document.createElement("button");
    slideoutBtn.innerText = "cooool";
    slideoutBtn.onclick = () => {
      div.classList.toggle("on");
    };
    shiftList.appendChild(slideoutBtn);
  }
  if (!firstLoad) {
    let hash = window.location.hash;
    let url = location.href;
    if (hash) {
      location.href = hash;
      history.replaceState(null, null, url);
    }
    firstLoad = true;
  }
}

function createListEditPopup() {
  const popup = document.createElement("dialog");
  popup.classList.add("create-shiftlist-popup");

  const head = document.createElement("div");
  head.classList.add("header");
  const title = document.createElement("h1");
  title.innerText = gettext("Edit Shiftlist");
  head.appendChild(title);
  popup.appendChild(head);

  const options = document.createElement("div");
  options.classList.add("options");

  const name = document.createElement("input");
  const nameLbl = document.createElement("label");
  name.id = "name";
  name.type = "text";
  name.maxLength = 300;
  name.value = list.name;
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
  date.value = list.date;
  dateLbl.htmlFor = "date";
  dateLbl.innerText = gettext("Date");
  options.appendChild(dateLbl);
  options.appendChild(date);

  const typeLbl = document.createElement("label");
  const type = document.createElement("select");
  type.id = "type";
  type.value = list.type;
  typeLbl.htmlFor = "type";
  typeLbl.innerText = gettext("Type");
  types.forEach((t) => {
    const option = document.createElement("option");
    option.innerText = t[1];
    option.value = t[0];
    if (t[0] == list.type) option.selected = true;
    type.appendChild(option);
  });
  const changeVisName = () => {
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
  changeVisName();
  type.onchange = changeVisName;
  options.appendChild(typeLbl);
  options.appendChild(type);

  const activeLbl = document.createElement("label");
  const active = document.createElement("input");
  active.id = "active";
  active.type = "checkbox";
  active.checked = list.is_active;
  activeLbl.htmlFor = "active";
  activeLbl.innerText = gettext("Active");
  options.appendChild(activeLbl);
  options.appendChild(active);

  popup.appendChild(options);

  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  const safe = document.createElement("button");
  safe.innerText = gettext("Safe");
  safe.onclick = () => {
    if (date.value) {
      if (type.value == "event" ? name.value : true) {
        safeShiftlist(name.value, date.value, type.value, active.checked);
      }
    }
  };
  bottom.appendChild(safe);
  const close = document.createElement("button");
  close.innerText = gettext("Close");
  close.onclick = () => {
    popup.close();
  };
  bottom.appendChild(close);
  popup.appendChild(bottom);

  // delete
  if (user.perms.shift_del) {
    const del = document.createElement("button");
    del.innerText = gettext("Delete");
    del.classList.add("red-btn");
    del.classList.add("del-btn");
    del.onclick = () => {
      if (
        prompt(gettext("Type 'DELETE' to delete this shiftlist")) == "DELETE"
      ) {
        deleteShiftlist();
      }
    };
    bottom.append(del);
  }
  return popup;
}

function showCreatePopup() {
  const popup = document.querySelector(".shift-create-popup");
  popup.replaceChildren();
  // title
  const title = document.createElement("h1");
  title.innerText = gettext("Create shift");
  popup.appendChild(title);
  // opties
  const opties = document.createElement("div");
  opties.classList.add("options");
  // date
  const date = document.createElement("input");
  const dateLbl = document.createElement("label");
  dateLbl.innerText = gettext("Date");
  dateLbl.htmlFor = "date";
  date.type = "date";
  date.id = "date";
  opties.appendChild(dateLbl);
  opties.appendChild(date);
  //start
  const start = document.createElement("input");
  const startLbl = document.createElement("label");
  startLbl.innerText = gettext("Start");
  startLbl.htmlFor = "start";
  start.type = "time";
  start.id = "start";
  opties.appendChild(startLbl);
  opties.appendChild(start);
  //end
  const end = document.createElement("input");
  const endLbl = document.createElement("label");
  endLbl.innerText = gettext("End");
  endLbl.htmlFor = "end";
  end.type = "time";
  end.id = "end";
  opties.appendChild(endLbl);
  opties.appendChild(end);
  // max
  const max = document.createElement("input");
  const maxLbl = document.createElement("label");
  maxLbl.innerText = gettext("Max shifters");
  maxLbl.htmlFor = "max";
  max.type = "number";
  max.id = "max";
  max.min = 0;
  max.max = 99;
  opties.appendChild(maxLbl);
  opties.appendChild(max);

  // info
  const info = document.createElement("input");
  const infoLbl = document.createElement("label");
  infoLbl.innerText = gettext("Extra Info");
  infoLbl.htmlFor = "info";
  info.type = "text";
  info.id = "info";
  info.maxLength = 500;
  opties.appendChild(infoLbl);
  opties.appendChild(info);

  popup.appendChild(opties);
  //bottom buttons
  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  // safe button
  const safe = document.createElement("button");
  safe.innerText = gettext("Safe");
  safe.onclick = () => {
    if (
      date.value != "" &&
      start.value != "" &&
      end.value != "" &&
      max.value != ""
    )
      createShift(date.value, start.value, end.value, max.value, info.value);
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
  // show
  popup.showModal();
}

function showEditPopup(shift) {
  const popup = document.querySelector(".shift-edit-popup");
  popup.replaceChildren();
  // title
  const head = document.createElement("div");
  head.classList.add("header");
  const title = document.createElement("h1");
  title.innerText = `${shift.string.slice(0, -5)} ${shift.start} - ${
    shift.end
  }`;
  // opties
  const opties = document.createElement("div");
  opties.classList.add("hidden");
  opties.classList.add("options");
  // date
  const date = document.createElement("input");
  const dateLbl = document.createElement("label");
  dateLbl.innerText = gettext("Date");
  dateLbl.htmlFor = "date";
  date.type = "date";
  date.id = "date";
  date.value = shift.date;
  opties.appendChild(dateLbl);
  opties.appendChild(date);
  //start
  const start = document.createElement("input");
  const startLbl = document.createElement("label");
  startLbl.innerText = gettext("Start");
  startLbl.htmlFor = "start";
  start.type = "time";
  start.id = "start";
  start.value = shift.start;
  opties.appendChild(startLbl);
  opties.appendChild(start);
  //end
  const end = document.createElement("input");
  const endLbl = document.createElement("label");
  endLbl.innerText = gettext("End");
  endLbl.htmlFor = "end";
  end.type = "time";
  end.id = "end";
  end.value = shift.end;
  opties.appendChild(endLbl);
  opties.appendChild(end);
  // max
  const max = document.createElement("input");
  const maxLbl = document.createElement("label");
  maxLbl.innerText = gettext("Max shifters");
  maxLbl.htmlFor = "max";
  max.type = "number";
  max.id = "max";
  max.min = 0;
  max.max = 99;
  max.value = shift.max;
  opties.appendChild(maxLbl);
  opties.appendChild(max);

  // info
  const info = document.createElement("input");
  const infoLbl = document.createElement("label");
  infoLbl.innerText = gettext("Extra Info");
  infoLbl.htmlFor = "info";
  info.type = "text";
  info.id = "info";
  info.maxLength = 500;
  info.value = shift.info;
  opties.appendChild(infoLbl);
  opties.appendChild(info);

  const saveMode = document.createElement("input");
  saveMode.type = "hidden";
  saveMode.value = "shifters";
  popup.appendChild(saveMode);
  const span = document.createElement("span");
  span.innerText = "settings";
  span.classList.add("material-symbols-outlined");
  span.onclick = () => {
    if (ul.classList.contains("hidden")) {
      ul.classList.remove("hidden");
      opties.classList.add("hidden");
      saveMode.value = "shifters";
    } else {
      ul.classList.add("hidden");
      opties.classList.remove("hidden");
      saveMode.value = "settings";
    }
  };

  title.appendChild(span);
  head.appendChild(title);
  popup.appendChild(head);
  // shifters
  const ul = document.createElement("ul");
  const li = document.createElement("li");
  const select = document.createElement("select");
  select.appendChild(document.createElement("option"));
  leden.forEach((lid) => {
    const option = document.createElement("option");
    option.innerText = lid.name;
    option.value = lid.id;
    select.appendChild(option);
  });
  li.appendChild(select);
  for (let i = 0; shift.max > i; i++) {
    const liC = li.cloneNode(true);
    const shifter = shift.shifters[i];
    if (shifter) {
      liC.firstChild.value = shifter.id;
    }
    ul.appendChild(liC);
  }
  popup.appendChild(ul);
  popup.appendChild(opties);
  // bottom buttons
  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  // safe button
  const safe = document.createElement("button");
  safe.innerText = gettext("Safe");
  safe.onclick = () => {
    if (saveMode.value == "shifters") safeShifters(shift, ul);
    else if (saveMode.value == "settings")
      safeShift(
        shift,
        date.value,
        start.value,
        end.value,
        max.value,
        info.value
      );
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
  // delete
  if (user.perms.shift_del) {
    const del = document.createElement("button");
    del.innerText = gettext("Delete");
    del.classList.add("red-btn");
    del.classList.add("del-btn");
    del.onclick = () => {
      if (confirm(gettext("Are you sure you want to delete this shift?"))) {
        deleteShift(shift);
      }
    };
    bottom.append(del);
  }
  // show
  popup.showModal();
}

async function safeShiftlist(name, date, type, active) {
  const actionInfo = {
    id: list.id,
    name: name,
    date: date,
    type: type,
    active: active,
  };
  const response = await manageShiftlistRequest(actionInfo, "safe_shiftlist");
  if (response.body.status == "succes") {
    list = {
      date: date,
      type: response.body.shiftlist_info.type,
      name: name,
      id: list.id,
      is_active: active,
      string: response.body.shiftlist_info.string,
    };
    shiftsToHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function createShift(date, start, end, max, info) {
  const shiftInfo = {
    date: date,
    start: start,
    end: end,
    max: max,
    shiftList: list.id,
    info: info,
  };
  const response = await createShiftRequest(shiftInfo);
  if (response.body.status == "succes") {
    shifts.push({
      date: response.body.shift_info.date,
      start: start,
      end: end,
      shifters: [],
      id: response.body.shift_info.id,
      max: max,
      string: response.body.shift_info.string,
      info: info,
    });
    shiftsToHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function safeShifters(shift, ul) {
  shift.shifters = [];
  [...ul.children].forEach((li) => {
    const select = li.firstChild;
    const selected = select.options[select.selectedIndex];
    if (select.value) {
      const shifter = {
        id: parseInt(selected.value),
        name: selected.innerText,
      };
      shift.shifters.push(shifter);
    }
  });
  // dit hier onder verwijdert dupplicate object
  // dit moet zo omdat objecten nie werken met set voor de dubs weg te halen
  // dit kan mss beter maar maakt niet super veel uit denk ik
  const newShifters = Array.from(
    new Set(shift.shifters.map(JSON.stringify))
  ).map(JSON.parse);
  const shiftersIds = shift.shifters.map((s) => parseInt(s.id));
  const actionInfo = {
    shiftId: shift.id,
    shifters: shiftersIds,
  };
  const response = await manageShiftRequest(actionInfo, "safe_shifters");
  if (response.body.status == "succes") {
    shift.shifters = newShifters;
    shiftsToHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function safeShift(shift, date, start, end, max, info) {
  const actionInfo = {
    shiftId: shift.id,
    date: date,
    start: start,
    end: end,
    max: max,
    info: info,
  };
  const response = await manageShiftRequest(actionInfo, "safe_shift");
  if (response.body.status == "succes") {
    shift.date = date;
    shift.start = start;
    shift.end = end;
    shift.max = max;
    shift.string = response.body.shift.string;
    shift.info = info;
    sortShifts();
    shiftsToHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function deleteShift(shift) {
  const actionInfo = {
    shiftId: shift.id,
  };
  const response = await manageShiftRequest(actionInfo, "delete_shift");
  if (response.body.status == "succes") {
    shifts.splice(shifts.indexOf(shift), 1);
    shiftsToHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function deleteShiftlist() {
  const actionInfo = {
    id: list.id,
  };
  const response = await manageShiftlistRequest(actionInfo, "delete_shiftlist");
  if (response.body.status == "succes") {
    window.location.href = "/shiften";
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function takeShift(shift) {
  const response = await request(shift.id, "add_shifter");
  if (response.body.status == "succes") {
    shift.shifters.push(user);
    shiftsToHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}
async function clearShift(shift) {
  const response = await request(shift.id, "remove_shifter");
  if (response.body.status == "succes") {
    shift.shifters = shift.shifters.filter((u) => u.id != user.id);
    shiftsToHTML(shifts, list, user);
  } else {
    alert(`Error: ${response.body.status}`);
  }
}
