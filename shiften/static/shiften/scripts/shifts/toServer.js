import { sendHttpAsync } from "/static/scripts/ajaxTools.js";
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

export async function manageShiftlistRequest(actionInfo, action) {
  const requestBody = {
    action: action,
    actionInfo: actionInfo,
  };
  const response = await sendHttpAsync("manage_shiftlist", "POST", requestBody);
  return response;
}
