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
      console.log(json.shifts);
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
  getCookie(cookieName) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, cookieName.length + 1) === cookieName + "=") {
          cookieValue = decodeURIComponent(
            cookie.substring(cookieName.length + 1)
          );
          break;
        }
      }
    }
    return cookieValue;
  }
  shiftsToHTML() {
    const body = document.querySelector(".content");
    const h1 = document.createElement("h1");
    const list = this.#shiftRepository.list;
    // h1.innerText = `${list.id} | ${list.date} (${list.type})`;
    h1.innerText = gettext(
      `${list.date.charAt(0).toUpperCase() + list.date.slice(1)} (${
        list.type
      }) | ${list.id}`
    );
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
        if (s.id == this.#user) li.classList.add("loggedshifter");
        ul.appendChild(li);
      });
      shiftDiv.appendChild(ul);
      const buttonDiv = document.createElement("div");
      buttonDiv.classList.add("shift-button-status");
      if (shift.shifters.map((s) => s.id).includes(this.#user)) {
        // Clearshift
        const button = document.createElement("button");
        button.value = shift.id;
        button.innerText = gettext("Clear shift");
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
          this.takeShift();
        };
        buttonDiv.appendChild(button);
      }
      shiftDiv.appendChild(buttonDiv);
      day.appendChild(shiftDiv);
      if (shiftdate != shift.date) {
        shiftdate = shift.date;
        body.appendChild(day);
      }
    });
  }

  async takeShift(event) {
    event.preventDefault();
    this.getCookie("csrftoken");
    const shiftId = event.target.value;
    let body = {
      shiftId: shiftId,
    };
    let props = {
      method: "POST",
      headers: {
        "X-CSRFToken": cookieValue,
      },
      mode: "same-origin",
    };

    if (body !== null && body !== undefined) {
      props.body = JSON.stringify(body);
    }

    try {
      const response = await fetch("signup_shift", props);
      const result_1 = await response.json();
      const resultObj = {
        ok: response.ok,
        body: result_1,
      };
      console.log(resultObj);
      this.shiftsToHTML();
    } catch (error) {
      throw error;
    }
  }
}
