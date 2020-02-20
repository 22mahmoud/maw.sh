<script>
  export let segment;
</script>

<nav>
  <ul class="flex py-8">
    <li class="mr-6">
      <span>/</span>
      <a
        class:hover:text-teal-200="{segment !== undefined}"
        class:text-teal-300="{segment === undefined}"
        href="."
      >
        home
      </a>
    </li>
    <li class="mr-6">
      <span>/</span>
      <a
        class:hover:text-teal-200="{segment !== 'about'}"
        class:text-teal-300="{segment === 'about'}"
        href="about"
      >
        about
      </a>
    </li>
    <li class="mr-6">
      <span>/</span>
      <a
        class:hover:text-teal-200="{segment !== 'blog'}"
        class:text-teal-200="{segment === 'blog'}"
        rel="prefetch"
        href="blog"
      >
        blog
      </a>
    </li>
  </ul>
</nav>

<style>

</style>
