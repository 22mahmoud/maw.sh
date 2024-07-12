---
title-prefix: Tags
template:
  tags: true
collections:
  - cmd: find src/thoughts src/blog src/leetcode/problems -type f -name "index.md" ! -path "src/thoughts/index.md" ! -path "src/blog/index.md" ! -path "src/leetcode/problems/index.md" ! -path "src/blog/tags/index.md"
    key: tags
    group-by: keywords
---
