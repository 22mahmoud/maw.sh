---
title-prefix: Tags
template:
  tags: true
collections:
  - cmd: find src/blog -type f -name "index.md" ! -path "src/blog/index.md" ! -path "src/blog/tags/index.md"
    key: tags
    group-by: keywords
---
