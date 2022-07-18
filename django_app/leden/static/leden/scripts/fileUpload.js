function photoUploadInit() {
  const upload = document.querySelector(".photo-upload");
  upload.onchange = () => {
    console.log(upload.files);
    if (upload.files[0].size > 2 * 1048576) {
      upload.value = "";
    }
  };
}
addLoadEvent(photoUploadInit);
