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
{#if !$preloading}
  <main
    transition:fade
    class="border-t-4 border-transparent bg-gray-900 text-gray-300 w-screen
    h-screen "
  >
    <div class="max-w-4xl h-full mx-auto flex flex-col">
      <Nav {segment} />
      <div class="h-full w-full flex flex-col">
        <slot />
      </div>
    </div>
  </main>
{:else}
  <div class="h-screen w-screen flex items-center content-center">
    <Loader />
  </div>
{/if}

<style>

</style>
