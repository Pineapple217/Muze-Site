function getCookie(cookieName) {
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

export async function sendHttpAsync(path, method, body) {
  let props = {
    method: method,
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    mode: "same-origin",
  };

  if (body !== null && body !== undefined) {
    props.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(path, props);
    const result_1 = await response.json();
    const resultObj = {
      ok: response.ok,
      body: result_1,
    };
    return resultObj;
  } catch (error) {
    throw error;
  }
}

export async function getData(path) {
  try {
    const href = window.location.href.split("#")[0];
    const request = await fetch(href + path);
    if (!request.ok) {
      throw new Error(`HTTP error: ${request.status}`);
    }
    const json = await request.json();
    return json;
  } catch (error) {
    alert(error);
  }
}
