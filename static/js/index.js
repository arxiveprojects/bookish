document.querySelectorAll('input[type="file"]').forEach((input) => {
  input.addEventListener("change", function (e) {
    const fileName = this.files[0]?.name || "No file chosen";
    const display = this.nextElementSibling;

    if (!display || !display.classList.contains("file-name")) {
      const fileNameDisplay = document.createElement("span");
      fileNameDisplay.className = "file-name ml-2 text-sm text-gray-500";
      this.parentNode.insertBefore(fileNameDisplay, this.nextSibling);
    }

    this.nextElementSibling.textContent = fileName;
  });
});
