---
date: 2024-07-04T02:55+03:00
thought: true
---

**site update**: 

Now, I just use relative paths for image URLs anywhere in my blog, and by using
#Pandoc's `walk_block` function, I can automatically import any file in any page
and change the path to be absolute in the build time.
