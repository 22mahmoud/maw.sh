<script>
  import { onMount } from 'svelte';
  let visible = false;
  onMount(() => {
    visible = true;
  });

  function typewriter(node, { speed = 77 }) {
    const valid =
      node.childNodes.length === 1 && node.childNodes[0].nodeType === 3;

    if (!valid) {
      throw new Error(
        `This transition only works on elements with a single text node child`
      );
    }

    const text = node.textContent;
    const duration = text.length * speed;

    return {
      duration,
      tick: t => {
        const i = ~~(text.length * t);
        node.textContent = text.slice(0, i);
      },
    };
  }
</script>

{#if visible}
  <p in:typewriter class="font-display text-6xl text-center">
    <slot />
  </p>
{/if}
