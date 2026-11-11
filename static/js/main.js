document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("plant-file");
  const label = document.getElementById("file-name");
  if (input && label) {
    input.addEventListener("change", () => {
      label.textContent = input.files && input.files.length
        ? input.files[0].name
        : "No image selected";
    });
  }
});
