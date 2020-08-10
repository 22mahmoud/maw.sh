<script>
  export let segment: string;
  const routes = [
    { key: undefined, value: 'Home' },
    { key: 'about', value: 'About' },
    { key: 'blog', value: 'Blog' },
  ];
</script>

<div class="absolute top-0 left-0 flex w-full ">
  <svg width="100%" height="40" style="overflow:visible">
    <defs>
      <pattern
        id="hex"
        patternUnits="userSpaceOnUse"
        patternTransform="translate(-3.5 0)"
        viewBox="-14 -16 28 48"
        width="26"
        height="66"
      >
        <g fill="none" stroke-width="1" stroke="currentcolor">
          <path
            d=" M0 -16 L-14 -8 L -14 8 L 0 16 L 14 8 L 14 -8 L 0 -16 z "
          ></path>
          <path
            d=" M0 -16 L-14 -8 L -14 8 L 0 16 L 14 8 L 14 -8 L 0 -16 z "
            transform="translate(14 24)"
          ></path>
          <g stroke-width="1" opacity="0.5">
            <path d=" M0 -16 L 0 0 M-14 8 L0 0 L14 8 "></path>
            <path
              d=" M0 -16 L 0 0 M-14 8 L0 0 L14 8 "
              transform="translate(14 24)"
            ></path>
            <path
              d=" M0 -16 L 0 0 M-14 8 L0 0 L14 8 "
              transform="translate(-14 24)"
            ></path>
          </g>
        </g>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#hex)"></rect>
  </svg>
</div>

<nav class="mt-12">
  <ul class="flex py-6">
    {#each routes as { key, value }}
      <li class="mx-6">
        <span>/</span>
        <a
          class="{segment === key ? 'text-teal-300' : 'hover:text-teal-200'}"
          href="/{key === undefined ? '.' : key}"
          rel="prefetch"
        >
          {value}
        </a>
      </li>
    {/each}
  </ul>
</nav>

<style>

</style>
