<script>
  import { onMount } from 'svelte';
  import { spring } from 'svelte/motion';
  import { fly } from 'svelte/transition';
  import { foodEmojis } from './emojis.js';

  const EMOJI_ZIE = 30;
  let isEmojieFoodEnabled = false;
  const getRandEmoji = () => foodEmojis[~~(Math.random() * foodEmojis.length)];
  let pos = spring({ x: -100, y: -100 }, { stiffness: 0.1 });
  let size = spring(EMOJI_ZIE);

  function handleMouseMove(event) {
    console.log(window);
    console.log(event);
    pos.set({
      x: event.pageX,
      y: event.pageY,
    });
  }

  function handleMouseDown() {
    isEmojieFoodEnabled = true;
    size.set(EMOJI_ZIE + 10);
  }

  function handleMouseUp() {
    isEmojieFoodEnabled = false;
    size.set(EMOJI_ZIE);
  }

  onMount(() => {
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('touchend', handleMouseUp);
    document.addEventListener('touchstart', handleMouseDown);
    document.addEventListener('mousedown', handleMouseDown);
  });

  let arr = Array.from({ length: 5 }).map(() => Math.random());
</script>

<div
  style="--pageY:{$pos.y}px; --pageX:{$pos.x}px; --fontSize:{$size}px"
  class="select-none cursor w-20 h-20 absolute"
>
  <span>🍑</span>

  <div class="flex">
    {#each arr as number}
      {#if isEmojieFoodEnabled}
        <span
          transition:fly="{{ y: 40 * number, duration: 800 }}"
          class="text-xs"
        >
          {getRandEmoji()}
        </span>
      {/if}
    {/each}
  </div>

</div>

<style>
  .cursor {
    top: calc(var(--pageY) + 20px);
    left: calc(var(--pageX) + 20px);
    font-size: var(--fontSize);
  }
</style>
