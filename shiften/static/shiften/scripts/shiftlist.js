import { Shift } from "./shift.js";
import { shiftRequest } from "./toServer.js";

export async function main() {
  const json = await getData();
  console.log(json);
  let list = json.list;
  let user = json.user;
  let shifts = maakShifts(json.shifts);
  shiftsToHTML(shifts, list, user);
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

function shiftsToHTML(shifts, list, user) {
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
  // body.appendChild(h1);
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
    shiftDiv.appendChild(h4);
    const ul = document.createElement("ul");
    ul.classList.add("shifters");
    let li;
    shift.shifters.forEach((s) => {
      li = document.createElement("li");
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
        console.log(shift);
        clearShift(shift.id, shift, shifts, list, user);
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
      // button.addEventListener("click", this.takeShift);
      button.onclick = () => {
        console.log(shift);
        takeShift(shift.id, shift, shifts, list, user);
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
}

async function takeShift(shiftId, shift, shifts, list, user) {
  const response = await shiftRequest(shiftId, "add_shifter");
  if (response.body.status == "done") {
    shift.shifters.push(user);
    shiftsToHTML(shifts, list, user);
  } else {
    alert(`Error: ${response.body.status}`);
  }
}
async function clearShift(shiftId, shift, shifts, list, user) {
  const response = await shiftRequest(shiftId, "remove_shifter");
  if (response.body.status == "done") {
    shift.shifters = shift.shifters.filter((u) => u.id != user.id);
    shiftsToHTML(shifts, list, user);
  } else {
    alert(`Error: ${response.body.status}`);
  }
}
