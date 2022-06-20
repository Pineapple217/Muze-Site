import { Shift } from "./shift.js";
export class ShiftRepository {
  #list;
  #shifts;

  constructor() {
    this.#shifts = [];
  }

  set list(v) {
    this.#list = v;
  }

  get list() {
    return this.#list;
  }

  get shifts() {
    return this.#shifts;
  }

  addShift(date, start, end, shifters, id, max) {
    this.#shifts.push(new Shift(date, start, end, shifters, id, max));
  }
}
