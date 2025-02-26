---
slug: week-1-leetcode
title-prefix: Week \#01 of Leetcode
date: 2024-06-08T00:00+03:00
description: week \#01 of leetcode grinding
keywords:
  - leetcode
  - problem-sovling
  - hash-map
  - two-pointer
category: leetcode
template:
  post: true
---

So this is my first week of my [LeetCode](/leetcode) grinding journey, and I want
to share my notes and the techniques I've learned and the problems I've solved
each week.

For solving the problems, I've created a new Git [repository](https://github.com/22mahmoud/leetcode)
and keep track of my answers by creating a directory for each problem with the
following structure:

```sh
problems
├── 1002_find_common_characters
│   ├── index.md        # showing the solutin and notes
│   ├── index.ts        # the optimal soltution
│   ├── bruteforce.ts   # a brute-force soltuion
│   └── index.test.ts   # testing useing vitest
```

### Techniques:

- **Two-Pointer/Sliding-window**

  [0167](/leetcode/problems/167-two-sum-ii-input-array-is-sorted) - [0209](/leetcode/problems/209-minimum-size-subarray-sum/) - [0003](/leetcode/problems/3-longest-substring-without-repeating-characters) - [0121](/leetcode/problems/121-best-time-to-buy-and-sell-stock)

  so in this technique we use two variables act like a pointers, to keep track
  the current window base on condation

- **Prefix-Sum**

  [0238](/leetcode/problems/232-product-of-array-except-self)

  I used this technique to solve the [Product of Array Except Self](/leetcode/problems/232_product_of_array_except_self)
  problem, But instead to use a prefix-sum we use here a prefix/suffix-product
  to get the answer.

- **Hash-Map**

  [0846](/leetcode/problems/846-hand-of-straights/) - [0409](/leetcode/problems/409-longest-palindrome/) - [1002](/leetcode/problems/1002-find-common-characters)

  Absolutely we have to have a problems that the true hero to solve it,
  just use hash-map.

  ![](hashmap-meme.jpg "a hand push a blue button called HASHMAP 'meme'")

- **kadane algorithm**

  [0053](/leetcode/problems/53-maximum-subarray/)

  an algorithm to solve find the largest sum of any contiguous sub-array, by
  maintaining two values `max_sum` and `current_sum` and compare between them
  each iteration and take the max values
