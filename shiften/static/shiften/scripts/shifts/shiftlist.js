import { Shift } from "./shift.js";
import { request, manageShiftRequest, createShiftRequest } from "./toServer.js";
import { getData } from "/static/scripts/ajaxTools.js";

let list;
let user;
let shifts;
let leden;

export async function main() {
  const json = await getData("/ajax");
  list = json.list;
  user = json.user;
  shifts = maakShifts(json.shifts);
  if (user.perms.shift_change) {
    leden = json.leden;
  }
  shiftsToHTML();
}

function maakShifts(shifts) {
  return shifts.map((shift) => {
    return new Shift(
      shift.date,
      shift.start,
      shift.end,
      shift.shifters,
      shift.id,
      shift.max
    );
  });
}

function shiftsToHTML() {
  const body = document.querySelector(".content");
  const header = document.querySelector(".main-header");
  const h1 = document.createElement("h1");
  const shiftList = document.getElementById("shiftlist");
  shiftList.replaceChildren();
  header.replaceChildren();
  h1.innerText = gettext(
    `${list.date.charAt(0).toUpperCase() + list.date.slice(1)} (${
      list.type
    }) | ${list.id}`
  );
  header.appendChild(h1);
  let shiftdate = "";
  let day;
  shifts.forEach((shift) => {
    if (shiftdate != shift.date) {
      const h3 = document.createElement("h3");
      h3.innerText = `${shift.date}`;
      shiftList.appendChild(h3);
      day = document.createElement("div");
      day.classList.add("day");
    }
    const shiftDiv = document.createElement("div");
    shiftDiv.classList.add("shift");
    const h4 = document.createElement("h4");
    h4.innerText = `${shift.start} - ${shift.end}`;
    if (user.perms.shift_change) {
      //Can EDIT
      h4.innerText += " ";
      const button = document.createElement("button");
      button.classList.add("edit-button");
      button.value = shift.id;
      button.onclick = () => {
        showEditPopup(shift);
      };
      h4.appendChild(button);
    }
    shiftDiv.appendChild(h4);
    const ul = document.createElement("ul");
    ul.classList.add("shifters");
    shift.shifters.forEach((s) => {
      let li = document.createElement("li");
      li.innerText = s.name;
      if (s.id == user.id) li.classList.add("loggedshifter");
      ul.appendChild(li);
    });
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
      const vol = document.createElement("p");
      vol.classList.add("volle-shift");
      vol.innerText = gettext("Shift Full");
      buttonDiv.appendChild(vol);
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
  if (user.perms.shift_add) {
    const add = document.createElement("button");
    add.innerText = gettext("Add shift");
    add.classList.add("add-shift-btn");
    add.onclick = () => {
      showCreatePopup();
    };
    header.appendChild(add);
    const popup = document.createElement("dialog");
    popup.classList.add("shift-create-popup");
    shiftList.appendChild(popup);
  }
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
  opties.classList.add("opties");
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
  //
  popup.appendChild(opties);
  //bottom buttons
  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  // safe button
  const safe = document.createElement("button");
  safe.innerText = gettext("Safe");
  safe.onclick = () => {
    createShift(date.value, start.value, end.value, max.value);
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
  title.innerText = `${shift.date} ${shift.start} - ${shift.end}`;
  head.appendChild(title);
  // delete
  if (user.perms.shift_del) {
    title.innerText += " ";
    const del = document.createElement("button");
    del.innerText = gettext("Delete");
    del.classList.add("delete-btn");
    del.onclick = () => {
      if (confirm(gettext("Are you sure you want to delete this shift?"))) {
        deleteShift(shift);
      }
    };
    head.append(del);
  }
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
  // const div = document.createElement("div");
  // div.classList.add("related-widget-wrapper");
  // div.appendChild(select);
  // li.appendChild(div);
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
  // bottom buttons
  const bottom = document.createElement("div");
  bottom.classList.add("bottom-btns");
  // safe button
  const safe = document.createElement("button");
  safe.innerText = gettext("Safe");
  safe.onclick = () => {
    safeShift(shift, ul);
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

function generateBottomButtons() {}

async function createShift(date, start, end, max) {
  const shiftInfo = {
    date: date,
    start: start,
    end: end,
    max: max,
    shiftList: list.id,
  };
  const response = await createShiftRequest(shiftInfo);
  if (response.body.status == "succes") {
    shifts.push(
      new Shift(
        response.body.shift_info.date,
        start,
        end,
        [],
        response.body.shift_info.id,
        max
      )
    );
    shiftsToHTML();
  } else {
    alert(`Error: ${response.body.status}`);
  }
}

async function safeShift(shift, ul) {
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
