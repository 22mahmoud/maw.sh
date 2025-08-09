document.addEventListener('htmx:afterRequest', event => {
  const detail = (event as CustomEvent).detail as { elt?: HTMLElement };
  const trigger = detail?.elt;

  if (trigger?.id === 'django-comments-xtd-reply') {
    document.querySelector('#comments-section')?.scrollIntoView({ behavior: 'smooth' });
  }
});
