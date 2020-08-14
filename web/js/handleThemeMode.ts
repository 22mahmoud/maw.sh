export const handleThemeMode = () => {
  const themeToggle: HTMLButtonElement = document.querySelector(
    '.theme-toggle'
  );

  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');

    const theme = document.body.classList.contains('dark-theme')
      ? 'dark'
      : 'light';

    document.cookie = `theme=${theme}`;
  });
};
