import { sendHttpAsync } from "/static/scripts/ajaxTools.js";

export async function creatShiftlistrequest(actionInfo, action) {
  const requestBody = {
    action: action,
    actionInfo: actionInfo,
  };
  const response = await sendHttpAsync("create_shiftlist", "POST", requestBody);
  return response;
}
