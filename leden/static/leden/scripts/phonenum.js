"use strict";
let oldL = "";

const formatnummer = function (event) {
  if (event.target.value === "") event.target.value = "+";
  let l = event.target.value.length;
  for (let i of [3, 7, 10, 13]) {
    if (l < oldL.length && l == i)
      event.target.value = event.target.value.slice(0, -1);
    if (l == i && l >= oldL.length) event.target.value += " ";
  }
  if (l > 16) event.target.value = event.target.value.slice(0, -1);
  oldL = event.target.value;
};

const nummer = document.getElementById("id_tel");
nummer.onfocus = formatnummer;
nummer.oninput = formatnummer;
