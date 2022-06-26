import { sendHttpAsync } from "/static/scripts/ajaxTools.js";
export async function creatShiftlistrequest(shiftlistInfo) {
  const response = await sendHttpAsync(
    "create_shiftlist",
    "POST",
    shiftlistInfo
  );
  return response;
}
