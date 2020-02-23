<script context="module">
  export function preload() {
    return this.fetch('sitemap.xml').then(() => this.fetch('robots.txt'));
  }
</script>

<script>
  import SEO from '../components/SEO.svelte';
</script>

<SEO />
<div class="h-full flex flex-col justify-center content-center">
  <div>
    <p class="font-display text-4xl md:text-6xl">
      Hi there 👋, I'm Mahmoud Ashraf a front-end developer
    </p>
    <p class="mt-5 text-xl font-light">- 🌍 🌊 Alexandria, Egypt</p>
  </div>
</div>

<style>

</style>
