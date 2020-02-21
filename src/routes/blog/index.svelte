<script context="module">
  export function preload({ params, query }) {
    return this.fetch(`blog.json`)
      .then(r => r.json())
      .then(posts => {
        return { posts };
      });
  }
</script>

<script>
  import format from 'date-fns/format';
  export let posts;
  $: console.log(posts);
  function formatDate(date) {
    return format(new Date(date), 'PP');
  }
</script>

<svelte:head>
  <title>Blog | Mahmoud Ashraf</title>
</svelte:head>

{#each posts as { title, slug, date, description, categories }}
  <article class="my-6">
    <header>
      <h3 class="font-bold text-2xl text-teal-300">
        <a rel="prefetch" href="blog/{slug}">{title}</a>
      </h3>
      <small>
        <date>{formatDate(date)}</date>
      </small>
      <div class="my-2 md:my-1">
        {#each categories as category}
          <span
            class="mr-2 px-2 bg-teal-800 hover:bg-teal-700 transation-all
            duration-200 ease-in rounded-md"
          >
            <a rel="prefetch" href="categories/{category}">{category}</a>
          </span>
        {/each}
      </div>
      <p class="text-base">{description}</p>
    </header>
  </article>
{/each}

<style>

</style>
