<script context="module">
  export async function preload({ params, query }) {
    const res = await this.fetch(`blog/${params.slug}.json`);
    const data = await res.json();
    if (res.status === 200) {
      return { post: data };
    } else {
      this.error(res.status, data.message);
    }
  }
</script>

<script>
  import { onMount } from 'svelte';
  export let post;
</script>

<svelte:head>
  <title>{post.meta.title}</title>
</svelte:head>

<h1>{post.meta.title}</h1>
<div>
  {@html post.content}
</div>

<style>

</style>
