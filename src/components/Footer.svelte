<script>
  let email = '';
  let firstName = '';
  function encode(data) {
    return Object.keys(data)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(data[key])}`)
      .join('&');
  }

  function handleSubmit() {
    fetch('https://mahmoudashraf.dev', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: encode({ 'form-name': 'subscription', email, firstName }),
    }).then(() => alert('success'));
  }
</script>

<div class="flex">
  <div class="flex flex-col p-6 bg-gray-800 shadow-xs rounded">
    <h3 class="text-lg mb-3 underline">Join the Newsletter</h3>
    <form
      on:submit|preventDefault="{handleSubmit}"
      class="flex flex-col"
      name="subscription"
      action="/"
      method="POST"
      data-netlify="true"
      data-netlify-honeypot="bot-field"
    >
      <label for="first_name" class="mb-1">First Name</label>
      <input
        bind:value="{firstName}"
        class="mb-2"
        name="first_name"
        placeholder="Mahmoud"
        type="text"
      />
      <label for="email" class="mb-1">Email</label>
      <input
        bind:value="{email}"
        name="email"
        placeholder="mahmoud@test.com"
        type="email"
      />
      <button
        class="px-4 py-2 bg-gray-700 rounded text-gray-200 mt-3 text-lg pointer
        shadow-xs hover:bg-gray-600 transition-all duration-200 ease-in"
        type="submit"
      >
        Subscribe
      </button>
    </form>
  </div>
</div>

<style>
  input {
    @apply px-3 py-1;
    @apply rounded;
    @apply border-0;
    @apply text-gray-700;
  }

  h3 {
    text-decoration-line: underline;
    text-decoration-style: wavy;
    text-decoration-color: #81e6d9;
    text-decoration-thickness: 1rem;
  }
</style>
