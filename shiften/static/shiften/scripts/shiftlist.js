import { Shift } from "./shift.js";
import { request, manageShiftRequest, createShiftRequest } from "./toServer.js";

let list;
let user;
let shifts;
let leden;

export async function main() {
  const json = await getData();
  list = json.list;
  user = json.user;
  shifts = maakShifts(json.shifts);
  if (user.perms.shift_change) {
    leden = json.leden;
  }
  shiftsToHTML();
}

async function getData() {
  try {
    const request = await fetch(window.location.href + "/ajax");
    if (!request.ok) {
      throw new Error(`HTTP error: ${request.status}`);
    }
    const json = await request.json();
    return json;
  } catch (error) {
    alert(error);
  }
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
  const h1 = document.querySelector(".content h1");
  const shiftList = document.getElementById("shiftlist");
  shiftList.replaceChildren();
  h1.innerHTML = "";
  h1.innerText = gettext(
    `${list.date.charAt(0).toUpperCase() + list.date.slice(1)} (${
      list.type
    }) | ${list.id}`
  );
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
    add.onclick = () => {
      showCreatePopup();
    };
    h1.appendChild(add);
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
  const list = document.createElement("ul");
  // date
  const date = document.createElement("input");
  const dateLi = document.createElement("li");
  date.type = "date";
  dateLi.appendChild(date);
  list.appendChild(dateLi);
  //start
  const start = document.createElement("input");
  const startLi = document.createElement("li");
  start.type = "time";
  startLi.appendChild(start);
  list.appendChild(startLi);
  //end
  const end = document.createElement("input");
  const endLi = document.createElement("li");
  end.type = "time";
  endLi.appendChild(end);
  list.appendChild(endLi);
  // max
  const max = document.createElement("input");
  const maxLi = document.createElement("li");
  max.type = "number";
  maxLi.appendChild(max);
  list.appendChild(maxLi);
  //
  popup.appendChild(list);
  // safe button
  const safe = document.createElement("button");
  safe.innerText = gettext("safe");
  safe.onclick = () => {
    createShift(date.value, start.value, end.value, max.value);
  };
  popup.appendChild(safe);
  // close button
  const close = document.createElement("button");
  close.innerText = gettext("Close");
  close.onclick = () => {
    popup.close();
  };
  popup.appendChild(close);
  // show
  popup.showModal();
}

function showEditPopup(shift) {
  const popup = document.querySelector(".shift-edit-popup");
  popup.replaceChildren();
  // title
  const title = document.createElement("h2");
  title.innerText = `${shift.date} ${shift.start} - ${shift.end}`;
  popup.appendChild(title);
  // delete
  if (user.perms.shift_del) {
    title.innerText += " ";
    const del = document.createElement("button");
    del.innerText = gettext("Delete");
    del.onclick = () => {
      if (confirm(gettext("Are you sure you want to delete this shift?"))) {
        deleteShift(shift);
      }
    };
    title.append(del);
  }
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
  // safe button
  const safe = document.createElement("button");
  safe.innerText = gettext("safe");
  safe.onclick = () => {
    safeShift(shift, ul);
  };
  popup.appendChild(safe);
  // close button
  const close = document.createElement("button");
  close.innerText = gettext("Close");
  close.onclick = () => {
    popup.close();
  };
  popup.appendChild(close);
  // show
  popup.showModal();
}

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
    shiftsToHTML(shifts, list, user);
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
