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
    pos.set({
      x: event.pageX,
      y: event.pageY,
    });
  }

  onMount(() => {
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', () => {
      isEmojieFoodEnabled = false;
      size.set(EMOJI_ZIE);
    });
    document.addEventListener('mousedown', () => {
      isEmojieFoodEnabled = true;
      size.set(EMOJI_ZIE + 10);
    });
  });
</script>

<div
  style="--pageY:{$pos.y}px; --pageX:{$pos.x}px; --fontSize:{$size}px"
  class="select-none cursor w-20 h-20 absolute"
>
  <span>🍑</span>
  {#if isEmojieFoodEnabled}
    <span transition:fly="{{ y: 20, duration: 500 }}" class="text-xs flex">
      {getRandEmoji()} {getRandEmoji()}{getRandEmoji()}{getRandEmoji()}
    </span>
  {/if}
</div>

<style>
  .cursor {
    top: calc(var(--pageY) + 20px);
    left: calc(var(--pageX) + 20px);
    font-size: var(--fontSize);
  }
</style>
