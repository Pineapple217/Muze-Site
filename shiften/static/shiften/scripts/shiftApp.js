import { ShiftRepository } from "./shiftRepository.js";
export class ShiftApp {
  #shiftRepository;
  #user;
  constructor() {
    this.#shiftRepository = new ShiftRepository();
    this.initHTML();
  }

  async initHTML() {
    await this.haalData();
    console.log(this.#shiftRepository.shifts);
    console.log(this.#shiftRepository.list);
    this.shiftsToHTML();
  }

  async haalData() {
    try {
      const request = await fetch(window.location.href + "/ajax");
      if (!request.ok) {
        throw new Error(`HTTP error: ${request.status}`);
      }
      const json = await request.json();
      this.#shiftRepository.list = json.list;
      this.#user = json.user;
      json.shifts.forEach((shift) => {
        this.#shiftRepository.addShift(
          shift.date,
          shift.start,
          shift.end,
          shift.shifters,
          shift.id,
          shift.max
        );
      });
    } catch (error) {
      alert(error);
    }
  }

  shiftsToHTML() {
    const body = document.querySelector(".content");
    const h1 = document.createElement("h1");
    const list = this.#shiftRepository.list;
    // h1.innerText = `${list.id} | ${list.date} (${list.type})`;
    h1.innerText = gettext(`${list.id} | ${list.date} (${list.type})`);
    console.log(gettext("Choose"));
    body.appendChild(h1);
    let shiftdate = "";
    let day;
    this.#shiftRepository.shifts.forEach((shift) => {
      if (shiftdate != shift.date) {
        const h3 = document.createElement("h3");
        h3.innerText = `${shift.date}`;
        body.appendChild(h3);
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
        ul.appendChild(li);
      });
      shiftDiv.appendChild(ul);
      const buttonDiv = document.createElement("div");
      buttonDiv.classList.add("shift-button-status");
      if (shift.shifters.map((s) => s.id).includes(this.#user)) {
        const button = document.createElement("button");
        button.value = shift.id;
        button.innerText = gettext("Take shift");
        buttonDiv.appendChild(button);
      } else if (shift.max <= shift.shifters.length) {
        console.log("max");
      }
      shiftDiv.appendChild(buttonDiv);
      day.appendChild(shiftDiv);
      if (shiftdate != shift.date) {
        shiftdate = shift.date;
        body.appendChild(day);
      }
    });
  }
}
