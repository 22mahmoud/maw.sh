<div class="content">
  <slot />
</div>

<style global>
  .content pre {
    overflow: auto;
    @apply rounded-md;
    @apply bg-gray-800;
    @apply my-4 p-3;
    @apply shadow-xs;
  }

  .content a {
    @apply transition-all ease-in duration-200;
    @apply text-teal-200;
  }

  .content p {
    @apply mb-6;
    @apply leading-loose;
    @apply text-lg;
  }

  .content h1,
  .content h2,
  .content h3 {
    @apply font-bold;
    @apply mt-8 mb-6;
  }

  .content h1 {
    @apply text-3xl;
  }

  .content h2 {
    @apply text-2xl;
  }

  .content h3 {
    @apply text-xl;
  }

  .content p code {
    @apply bg-gray-700;
    @apply text-gray-400;
    @apply p-1;
    @apply rounded;
  }

  .content blockquote {
    @apply border-l-4 border-teal-200;
    @apply pl-5;
    @apply italic;
  }

  .content ul {
    @apply list-disc list-inside;
  }

  .content li {
    @apply mb-3;
  }
</style>
