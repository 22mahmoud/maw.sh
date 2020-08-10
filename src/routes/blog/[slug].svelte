<script context="module">
  // @ts-ignore
  export async function preload({ params, query }) {
    // @ts-ignore
    const res = await this.fetch(`blog/${params.slug}.json`);
    const data = await res.json();
    if (res.status === 200) {
      return { post: data };
    } else {
      // @ts-ignore
      this.error(res.status, data.message);
    }
  }
</script>

<script>
  import SEO from "../../components/SEO.svelte";
  import MdLayout from "../../components/MdLayout.svelte";
  export let post: any;
</script>

<style>

</style>

<SEO
  title={post.meta.title}
  description={post.meta.description}
  keywords={post.meta.keywords}
  slug={post.meta.slug} />

<h1 class="my-8 text-2xl font-bold">{post.meta.title}</h1>

<MdLayout>
  {@html post.content}
</MdLayout>
