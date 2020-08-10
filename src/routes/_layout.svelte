<script>
  import { stores } from "@sapper/app";
  import PageLoadingBar from "sapper-page-loading-bar/PageLoadingBar.svelte";

  import Nav from "../components/Nav.svelte";
  import Footer from "../components/Footer.svelte";

  export let segment: string;
  const { preloading } = stores();
</script>

<style global>
  @import "../styles/index.css";
</style>

<svelte:head>
  <script
    data-goatcounter="https://stats.mahmoudashraf.dev/count"
    async
    src="//stats.mahmoudashraf.dev/count.js">

  </script>
</svelte:head>
<PageLoadingBar {preloading} />
<div class="flex flex-col w-full min-h-screen">
  <div class="flex-1">
    <header class="w-full my-3">
      <div class="max-w-2xl mx-auto">
        <Nav {segment} />
      </div>
    </header>

    <main class="flex flex-col max-w-2xl px-4 mx-auto md:px-2">
      <slot />
    </main>
  </div>

  <footer class="w-full">
    <div class="max-w-2xl px-4 mx-auto my-24 md:px-2">
      <Footer />
    </div>
  </footer>
</div>
