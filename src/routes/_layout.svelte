<script>
  import { stores } from '@sapper/app';
  import { fade } from 'svelte/transition';
  import PageLoadingBar from 'sapper-page-loading-bar/PageLoadingBar.svelte';

  import Nav from '../components/Nav.svelte';
  import Footer from '../components/Footer.svelte';
  import Tailwindcss from '../components/Tailwindcss.svelte';

  export let segment;
  const { preloading } = stores();
</script>

<Tailwindcss />
<PageLoadingBar {preloading} />
<div class="flex flex-col min-h-screen w-full">
  <div class="flex-1">
    <header class="w-full my-3">
      <div class="max-w-2xl mx-auto">
        <Nav {segment} />
      </div>
    </header>

    {#if !$preloading}
      <main class="max-w-2xl flex flex-col mx-auto px-4 md:px-2">
        <slot />
      </main>
    {/if}
  </div>

  <footer class="border-t-2 border-gray-800 mt-6 w-full">
    <div class="py-6 max-w-2xl mx-auto px-4 md:px-2">
      <Footer />
    </div>
  </footer>
</div>

<style>

</style>
