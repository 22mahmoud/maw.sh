<script>
  import Nav from '../components/Nav.svelte';
  import { onMount } from 'svelte';
  import { spring } from 'svelte/motion';
  /* export let segment; */

  const EMOJI_ZIE = 30;
  let pos = spring({ x: -100, y: -100 }, { stiffness: 0.1 });
  let size = spring(EMOJI_ZIE);

  function handleMouseMove(event) {
    pos.set({
      x: event.clientX,
      y: event.clientY,
    });
  }
</script>

<main
  on:mousemove="{handleMouseMove}"
  on:mousedown="{() => size.set(EMOJI_ZIE + 10)}"
  on:mouseup="{() => size.set(EMOJI_ZIE)}"
  class="bg-gray-900 text-gray-300 w-screen h-screen "
>
  <svg class="w-full h-full absolute p-3">
    <text x="{$pos.x}" y="{$pos.y}" font-size="{$size}">🍑</text>
  </svg>

  <div class="max-w-4xl mx-auto">
    <slot />
  </div>

</main>

<style>

</style>
