<script>
  import { onMount } from 'svelte';
  import lottie from 'lottie-web';
  import animationData from './confusion-lottie.json';

  let loading;
  onMount(async () => {
    let animation = null;
    const options = {
      container: loading,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      animationData,
    };
    animation = lottie.loadAnimation(options);
    return () => animation && animation.destroy();
  });
</script>

<p bind:this="{loading}" class="w-20 m-auto"></p>
