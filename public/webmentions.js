document.addEventListener("DOMContentLoaded", function () {
  function getRandomColor() {
    const hue = Math.floor(Math.random() * 360);
    const saturation = Math.floor(Math.random() * 50) + 50;
    const lightness = 80;

    return `hsla($${hue}, $${saturation}%, $${lightness}%, 0.4)`;
  }

  document
    .querySelectorAll(".bookmark-item img")
    .forEach((x) => x.style.setProperty("--hover-color", getRandomColor()));
});
