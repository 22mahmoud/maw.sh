<script>
  import siteMetadata from '../../config/siteMetaData.js';
  export let title = siteMetadata.title;
  export let description = siteMetadata.description;
  export let keywords = siteMetadata.keywords;
  export let slug = null;
  export let thumb = `https://mahmoudashraf.dev/${siteMetadata.image}`;
</script>

<svelte:head>
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="{slug ? 'article' : 'website'}" />
  <meta
    property="og:url"
    content="{slug ? `${siteMetadata.siteUrl}${slug}` : siteMetadata.siteUrl}"
  />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  {#if thumb}
    <meta property="og:image" content="{thumb}" />
  {/if}

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta
    property="twitter:url"
    content="{slug ? `${siteMetadata.siteUrl}${slug}` : siteMetadata.siteUrl}"
  />
  <meta property="twitter:title" content="{title}" />
  <meta property="twitter:description" content="{description}" />
  {#if thumb}
    <meta property="twitter:image" content="{thumb}" />
  {/if}
</svelte:head>
