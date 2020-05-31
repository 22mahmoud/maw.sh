<script context="module">
  export function preload() {
    return this.fetch('sitemap.xml').then(() => this.fetch('robots.txt'));
  }
</script>

<script>
  import SEO from '../components/SEO.svelte';
  import { _ } from 'svelte-i18n';
  const m = 'lol';
</script>

<SEO />
<div class="flex flex-col content-center justify-center h-full">
  <div>
    <p class="text-4xl font-display md:text-6xl">
      Hi there 👋, I'm {$_('page_title')} a front-end developer
    </p>
    <p class="mt-5 text-xl font-light">- 🌍 🌊 Alexandria, Egypt</p>
  </div>
</div>

<style>

</style>
