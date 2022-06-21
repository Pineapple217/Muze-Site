export class Shift {
  date;
  start;
  end;
  shifters;
  id;
  max;
  constructor(date, start, end, shifters, id, max) {
    this.date = date;
    this.start = start;
    this.end = end;
    this.shifters = shifters;
    this.id = id;
    this.max = max;
  }

  // get date() {
  //   return this.#date;
  // }

  // get start() {
  //   return this.#start;
  // }

  // get end() {
  //   return this.#end;
  // }

  // get shifters() {
  //   return this.#shifters;
  // }

  // get id() {
  //   return this.#id;
  // }

  // get max() {
  //   return this.#max;
  // }
}
