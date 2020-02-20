<script>
  import Nav from '../components/Nav.svelte';
  import Cursor from '../components/Cursor/index.svelte';
  /* export let segment; */
</script>

<Cursor />
<main class="bg-gray-900 text-gray-300 w-screen h-screen ">
  <div class="max-w-4xl h-full mx-auto">
    <slot />
  </div>
</main>
