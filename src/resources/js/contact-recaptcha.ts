import htmx from 'htmx.org';

(() => {
  const contactForm = document.getElementById('contact-form') as HTMLFormElement | null;
  if (!contactForm) {
    return;
  }

  const tokenInput = document.getElementById(
    'contact-recaptcha-token-input',
  ) as HTMLInputElement | null;

  if (!tokenInput) {
    console.error('The hidden reCAPTCHA input "#recaptcha-token-input" was not found.');
    return;
  }

  const siteKey = import.meta.env.VITE_RECAPTCHA_SITE_KEY;

  if (!siteKey) {
    console.error('VITE_RECAPTCHA_SITE_KEY is not defined in your .env file.');
    return;
  }

  const handleSubmit = async (event: SubmitEvent) => {
    event.preventDefault();

    grecaptcha.ready(async () => {
      try {
        const token = await grecaptcha.execute(siteKey, {
          action: 'signup',
        });
        tokenInput.value = token;
        htmx.trigger(contactForm, 'recaptchaSubmit');
      } catch (error) {
        console.error('Failed to execute reCAPTCHA:', error);
      }
    });
  };

  contactForm.addEventListener('submit', handleSubmit);
})();
