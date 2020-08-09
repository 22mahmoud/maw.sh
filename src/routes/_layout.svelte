<script>
  import Nav from "../components/Nav.svelte";

  export let segment: string;
</script>

<style global>
  @import "../global.css";
</style>

<Nav {segment} />

<main>
  <slot />
</main>
