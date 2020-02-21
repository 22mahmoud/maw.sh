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
<header class="max-w-2xl flex mx-auto my-4">
  <Nav {segment} />
</header>

{#if !$preloading}
  <main class="max-w-2xl flex flex-col mx-auto px-4 md:px-2">
    <slot />
  </main>
{:else}
  <dev
    style="width: 50px; height: 50px;"
    class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2
    h-full"
  >
    <Loader />
  </dev>
{/if}

<style>

</style>
