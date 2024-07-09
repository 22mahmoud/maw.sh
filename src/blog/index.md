---
title-prefix: Blog
pagination:
  collection: blog
  cmd: find src/blog -type f -name "index.md" ! -path "src/blog/index.md" ! -path "src/blog/tags/index.md"
  page-size: 30
  page-path: page
header-includes: |-
  <style>
    br {
      display: none;
    }

    img, video {
      aspect-ratio: 16 / 9;
      object-fit: contain;
    }

    .blog .navigation {
      text-align: right;
      margin-top: 10px;
    }

    .blog .navigation a {
      margin-left: 10px;
    }
  </style>
---

