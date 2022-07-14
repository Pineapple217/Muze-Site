const templateInit = function () {
  const textarea = document.getElementById("id_template");
  function formatJSON() {
    try {
      textarea.value = JSON.stringify(JSON.parse(textarea.value), null, 2);
    } catch (e) {
      console.log("not valid JSON");
    }
  }
  formatJSON();
  textarea.onchange = formatJSON;
  textarea.onauxclick = formatJSON;
};
addLoadEvent(templateInit);
