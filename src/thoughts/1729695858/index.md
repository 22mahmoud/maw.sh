---
date: 2024-10-23T18:04:18+03:00
template:
  thought: true
keywords:
  - snippets
  - git
---

A quick snippet to keep your local Git branches in sync with the remote by
removing deleted branches:

```sh
alias gcln='git fetch -p && git branch -vv \
  | grep ": gone]" \
  | awk "{print \$1}" \
  | xargs -r git branch -D'
```
