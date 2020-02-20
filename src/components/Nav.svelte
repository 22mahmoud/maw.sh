<script>
  export let segment;
  const routes = [
    { key: undefined, value: 'Home' },
    { key: 'about', value: 'About' },
    { key: 'blog', value: 'Blog' },
  ];
</script>

<nav>
  <ul class="flex py-8">
    {#each routes as { key, value }}
      <li class="mx-6">
        <span>/</span>
        <a
          class="{segment === key ? 'text-teal-300' : 'hover:text-teal-200'}"
          href="/{key === undefined ? '.' : key}"
        >
          {value}
        </a>
      </li>
    {/each}
  </ul>
</nav>

<style>

</style>
