function getRandomColor() {
  const hue = Math.floor(Math.random() * 360);
  const saturation = Math.floor(Math.random() * 20) + 60;
  const lightness = Math.floor(Math.random() * 15) + 75;

  return `hsla(${hue}, ${saturation}%, ${lightness}%, 0.6)`;
}

document
  .querySelectorAll('.bookmark-item img')
  .forEach((x) => x.style.setProperty('--hover-color', getRandomColor()));
