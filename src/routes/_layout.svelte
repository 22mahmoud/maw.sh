<script>
  import { stores } from '@sapper/app';
  import { fade } from 'svelte/transition';
  import PageLoadingBar from 'sapper-page-loading-bar/PageLoadingBar.svelte';
  import Loader from '../components/Loader.svelte';

  import Nav from '../components/Nav.svelte';
  export let segment;
  const { preloading } = stores();
</script>

<PageLoadingBar {preloading} />
<main
  class="border-t-4 border-transparent bg-gray-900 text-gray-300 w-screen
  h-screen "
>
  <div transition:fade class="max-w-4xl h-full mx-auto flex flex-col">
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
