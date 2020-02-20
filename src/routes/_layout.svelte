<script>
  import { stores } from '@sapper/app';
  import { fade } from 'svelte/transition';
  import PageLoadingBar from 'sapper-page-loading-bar/PageLoadingBar.svelte';
  import Loader from '../components/Loader.svelte';

  import Nav from '../components/Nav.svelte';
  import Cursor from '../components/Cursor/index.svelte';
  export let segment;
  const { preloading } = stores();
</script>

<Cursor />
<PageLoadingBar color1="#81e6d9" color2="#4FD1C5" {preloading} />
<main transition:fade class="bg-gray-900 text-gray-300 w-screen h-screen ">
  <div class="max-w-4xl h-full mx-auto flex flex-col">
    {#if !$preloading}
      <Nav {segment} />
      <slot />
    {:else}
      <Loader />
    {/if}
  </div>
</main>

<style>

</style>
