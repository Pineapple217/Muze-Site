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
}
