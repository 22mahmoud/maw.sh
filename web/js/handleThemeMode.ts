export const handleThemeMode = () => {
  const themeToggle: HTMLButtonElement = document.querySelector(
    '.theme-toggle'
  );

  const darkTheme: HTMLLinkElement = document.querySelector(
    'link[title="dark-theme"]'
  );
  const lightTheme: HTMLLinkElement = document.querySelector(
    'link[title="light-theme"]'
  );

  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');

    const theme = document.body.classList.contains('dark-theme')
      ? 'dark'
      : 'light';

    if (theme === 'dark') {
      lightTheme.disabled = true;
      darkTheme.disabled = false;
    } else if (theme === 'light') {
      lightTheme.disabled = false;
      darkTheme.disabled = true;
    }

    document.cookie = `theme=${theme}`;
  });
};
