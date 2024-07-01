---
slug: week-2-leetcode
title-prefix: Week \#02 of Leetcode
date: 2024-06-16T00:00+03:00
description: week \#02 of leetcode grinding
keywords:
  - leetcode
  - problem sovling
  - backtracking
  - Linkedlist
category: leetcode
blog: true
---

- This week I've built a [shell script](https://github.com/22mahmoud/leetcode/blob/main/bin/new) to generate a boilerplate for the problem
  from `leetcode` graphql api
  just run:
  ```shell
  ./bin/new :slug:
  ```
  and this will generate `index.md` with all metadata for the problem, `index.ts`
  which contains the function, and `index.test.ts` which contains a generic test
  case (TODO: will make it dynamic to get test cases from the api).

- Also a new design for leetcode problem page with native html `details` tag for
  description

  ![a screenshot of word search leetcode problem from my website](/blog/week-2-leetcode/screenshot-240616-0251-35.png)

- and a github [workflow](https://github.com/22mahmoud/leetcode/blob/main/.github/workflows/update_problems.yml) to generate the [/leetcode](/leetcode) page and commit
the changes into the leetcode branch, and after that get finished will trigger
[another one](https://github.com/22mahmoud/leetcode/blob/main/.github/workflows/update_blog.yml) to build my main website to get the latest changes

### Techniques:

- **Prefix-Sum**

  [0974](/leetcode/problems/974_subarray_sums_divisible_by_k/) - [0523](/leetcode/problems/523_continuous_subarray_sum/)

  So more prefix-sum problems, just to get comfort with the concept

- **Backtracking**

  [0017](/leetcode/problems/17_letter_combinations_of_a_phone_number/) - [0079](/leetcode/problems/79_word_search/) - [0078](/leetcode/problems/78_subsets/) - [0022](/leetcode/problems/22_generate_parentheses/)

  I spend most of this week to get understand backtracking, it kinda challenging
  at the beginning, but after you get the pattern, you will crush any backpacking
  problem, and the main key for to get the constrains and base case by illustrate
  the problem and solution by hand in the paper first.

- **Lined-List**

  [0206](/leetcode/problems/206_reverse_linked_list/)

  I just solved one easy problem, and start to implement (WIP) the `linkedlist`
  data stricture using typescript

