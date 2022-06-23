export async function request(shiftId, action) {
  //actions: add_shifter, remove_shifter
  const requestBody = {
    action: action,
    shiftId: shiftId,
  };
  const response = await sendHttpAsync("signup_shift", "POST", requestBody);
  return response;
}

export async function manageShiftRequest(actionInfo, action) {
  const requestBody = {
    action: action,
    actionInfo: actionInfo,
  };
  const response = await sendHttpAsync("manage_shift", "POST", requestBody);
  return response;
}

export async function createShiftRequest(shiftInfo) {
  const response = await sendHttpAsync("create_shift", "POST", shiftInfo);
  return response;
}

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

async function sendHttpAsync(path, method, body) {
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
