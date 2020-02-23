<script>
  import { fade, fly } from 'svelte/transition';
  let firstName = '';
  let email = '';
  let isSubmitting = false;
  let done = false;

  function handleSubmit() {
    isSubmitting = true;
    if (email && firstName) {
      fetch('/.netlify/functions/mailgun', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
        },
        body: JSON.stringify({ email, name: firstName }),
      }).then(() => {
        isSubmitting = false;
        done = true;
      });
    }
  }
</script>

<div class="flex">
  <div
    class="min-4 duration-400 w-full flex flex-col p-8 md:w-2/4 bg-gray-800
    shadow-xs rounded"
  >
    {#if !done}
      <div transition:fade="{{ duration: 400 }}">
        <h3 class="text-xl mb-8">Join the Newsletter 📰</h3>
        <form
          on:submit|preventDefault="{handleSubmit}"
          class="flex flex-col"
          name="subscription"
        >
          <label for="firstName" class="mb-2">First Name</label>
          <input
            bind:value="{firstName}"
            required
            class="mb-3"
            id="firstName"
            name="firstName"
            placeholder="Mahmoud"
            type="text"
          />
          <label for="email" class="mb-2">Email</label>
          <input
            bind:value="{email}"
            required
            id="email"
            name="email"
            placeholder="mahmoud@test.com"
            type="email"
          />
          <button
            disabled="{isSubmitting}"
            class="self-start px-5 py-3 bg-gray-700 rounded text-gray-200 mt-4
            text-lg pointer shadow-xs hover:bg-gray-600 transition-all
            duration-200 ease-in"
            type="submit"
          >
            {#if isSubmitting}loading...{:else}Subscribe{/if}
          </button>
        </form>
      </div>
    {:else}
      <div in:fly="{{ delay: 400, y: 100, duration: 1000 }}">
        <h2 class="text-left mb-8 text-2xl font-bold">
          Thank you for subscribing 💙
        </h2>
      </div>
    {/if}
  </div>
</div>

<style>
  input {
    @apply px-3 py-2;
    @apply rounded;
    @apply border-0;
    @apply text-gray-700;
  }

  h3 {
    text-decoration-line: underline;
    text-decoration-style: wavy;
    text-decoration-color: #81e6d9;
    text-decoration-thickness: 5rem;
  }
</style>
