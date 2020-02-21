<script>
  import { stores } from '@sapper/app';
  import { fade } from 'svelte/transition';
  import PageLoadingBar from 'sapper-page-loading-bar/PageLoadingBar.svelte';

  import Nav from '../components/Nav.svelte';
  import Tailwindcss from '../components/Tailwindcss.svelte';

  export let segment;
  const { preloading } = stores();
</script>

<Tailwindcss />
<PageLoadingBar {preloading} />
<header class="max-w-2xl flex mx-auto my-4">
  <Nav {segment} />
</header>

{#if !$preloading}
  <main class="max-w-2xl flex flex-col mx-auto px-4 md:px-2">
    <slot />
  </main>
{/if}

<style>

</style>
