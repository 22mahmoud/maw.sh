import '../styles/main.css';

document.addEventListener('DOMContentLoaded', () => {
  let counter = 0;
  const counterBtn = document.querySelector('.counter');

  counterBtn.addEventListener('click', () => {
    counter += 1;
    console.log(counter, 'w');
  });
});
