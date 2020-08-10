<script context="module">
  export function preload() {
    // @ts-ignore
    return this.fetch(`blog.json`)
      .then((r: any) => r.json())
      .then((posts: any[]) => {
        return { posts };
      });
  }
</script>

<script>
  import format from "date-fns/format";
  import SEO from "../../components/SEO.svelte";
  export let posts: any[];
  function formatDate(date: string = Date()) {
    return format(new Date(date), "PP");
  }
</script>

<style>

</style>

<SEO title="Blog | Mahmoud Ashraf" description="Mahmoud Ashraf blog posts" />
{#each posts as { title, slug, date, description }}
  <article class="my-6">
    <header>
      <h3 class="text-2xl font-bold text-teal-300">
        <a rel="prefetch" href="blog/{slug}">{title}</a>
      </h3>
      <small>
        <date>{formatDate(date)}</date>
      </small>
      <div class="my-2 md:my-1">
        <p class="text-base">{description}</p>
      </div>
    </header>
  </article>
{/each}
