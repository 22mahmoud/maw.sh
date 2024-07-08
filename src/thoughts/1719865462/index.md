---
date: "2024-07-01T20:24:00+00:00"
thought: true
---

**site update**:

Now with this [collection](https://github.com/22mahmoud/maw.sh/blob/master/filters/collections.lua)
#script i can build pages using #lua filters with convenient way by create the markdown page with
front matter metadata and it will populate all collection data to #pandoc filter

```md
# src/index.md
---
title-prefix: Home
home: true
collections:
  - name: games
    key: completed
    filter-by:
      key: state
      value: completed
    first: 3
  - name: blog
    first: 3
  - name: thoughts
    first: 3
    content: true
---
```
