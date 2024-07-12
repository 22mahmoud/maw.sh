---
date: "2024-07-03T23:55:00+00:00"
template:
  thought: true
keywords:
  - site-update
---

**site update**:

Now, I just use relative paths for image URLs anywhere in my blog, and by using
#Pandoc's `walk_block` function, I can automatically import any file in any page
and change the path to be absolute in the build time.
