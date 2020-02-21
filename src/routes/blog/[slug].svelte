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
  import SEO from '../../components/SEO.svelte';
  export let post;
</script>

<SEO
  title="{post.meta.title}"
  description="{post.meta.description}"
  keywords="post.meta.keywords"
  slug="{post.meta.slug}"
/>
<h1>{post.meta.title}</h1>
<div>
  {@html post.content}
</div>

<style>

</style>
