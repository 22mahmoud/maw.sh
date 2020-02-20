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
  <main class="max-w-2xl flex mx-auto px-4 md:px-2">
    <slot />
  </main>
{:else}
  <div class="h-screen w-screen flex items-center content-center">
    <Loader />
  </div>
{/if}

<style>

</style>
