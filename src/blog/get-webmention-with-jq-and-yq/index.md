---
slug: get-webmention-with-jq-and-yq
title-prefix: Get webmentions with shell script using jq & yq
date: 2024-06-29T00:00+03:00
description: In this article I'll demonstrate how I fetch this websites webmentions just using shell script.
keywords:
  - webmentions
  - shell
  - jq
  - yq
category: shell
blog: true
featured-image: /blog/get-webmention-with-jq-and-yq/hand-in-hand.jpg
---

Recently, I discovered that I can track the likes, reposts, and comments on
social media posts that include a links to any blog post or thought from my
website using webmentions. To learn more about webmentions, you can visit the
[indieweb](https://indieweb.org/Webmention).

This article will not cover how to set up webmentions on your blog, instead, it
will demonstrate how to use `jq` and `yq` to fetch webmentions and save them in
your Git repository.

![michelangelo touch of god drawing](/blog/get-webmention-with-jq-and-yq/hand-in-hand.jpg)

## What are `jq` and `yq` ?

Both tools do the same thing but with different file types. The first one, `jq`,
is a tool that can work with any `JSON` text to extract or set any value.
Similarly, `yq` serves the same purpose but is designed for `YAML` files.

## Create a shell script skeleton

Let's create a shell script named `webmention` and give it the executable
permissions `chmod +x webmention`

```shell
#!/bin/sh

base_url="https://webmention.io/api/mentions.jf2"
domain="<your-domain>"
token="<your-webmention-token>"

main() {
  # main script will be here
}

main
```

## How To fetch recent webmentions only

I need to run the script periodically, So I want to avoid over fetching every
time I fetch webmentions, and fortunately `webmentions.io` have a query-param
called `since` which only return webmentions after this date.

```shell
# [!code word:since=2024-06-29T15\:37\:22Z]

fetch_webmentions() {
  curl -s \
    "$base_url?since=2024-06-29T15:37:22Z&domain=$domain&token=$token"
}

```

So to keep track of the date, we need to save this data somewhere in the
codebase, and since i have `metadata.yaml` file, So why not to save it there.

```yaml
# metadata.yaml

title: Mahmoud Ashraf
# ...
last_webmention_sync: "2024-06-29T15:37:22Z"
```

```shell
# [!code word:since=$since]
since=$(yq ".last_webmention_sync" metadata.yaml)

fetch_webmentions() {
  curl -s \
    "$base_url?since=$since&domain=$domain&token=$token"
}
```

Finally after finish the whole script which will be showen latter on this blog,
we need to save the latest date to `yaml` file, so wen can use it the next run
of `webmention` script.

```shell
main() {
  # our script ...

  new_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  yq -i ".last_webmention_sync = \"$new_date\"" metadata.yaml
}
```


## How to format the `json` response

we need to transform the actual response of the `webmention` api, from this
format:

```jsonc
{
  "type": "feed",
  "name": "Webmentions",
  "children": [
    {
      "type": "entry",
      "wm-id": 1835832,
      "wm-target": "https://maw.sh/blog/build-a-blog-with-svelte-and-markdown/",
      "wm-property": "in-reply-to",
      // ...
    },
    // more entries
  ]
}
```

To this format:

```jsonc
[
  {
    "target": "blog/build-a-blog-with-svelte-and-markdown",
    "properties": [
      {
        "property": "in-reply-to",
        "entries": [{ "type": "entry", /* ... */ }]
      },
      { "property": "likes-of", "entries": [ /* ... */ ] }
    ]
  }
]
```

So we need to process the `json` like that:

1. remove my domain from each `wm-target`, so we can get the actual path
1. filter-out any webmentions for the home page "https://maw.sh/"
1. group-by the `wm-target` so now have an array of arrays grouped by the same
   target
1. after that map each to be an object with `target` and `properties`
   and `properties` will contain array of e.g: `{"property": "likes-of", "entries": []}`


```shell
format_output() {
	jq --arg domain "$domain" '.children
  | map(.["wm-target"] |= sub("^https://\($domain)/"; "")
                       | .["wm-target"] |= sub("/$"; ""))
  | map(select(.["wm-target"] != ""))
  | group_by(.["wm-target"])
  | map({
      target: .[0]["wm-target"],
      properties: group_by(.["wm-property"])
        | map({ property: .[0]["wm-property"], entries: .})
    })'
}

# ...

main () {
  fetch_webmentions | format_output
}
```

## Loop through each target and save the data

Now We need to go through each target and save the data in `yaml` format, or in
`json` but for me, I will go with `yaml` becuase i will use this file latter
with pandoc as metadata to display the webmentions

So with `-c,--compact-output`, jq will print each object into spreate line so we
iterate with while loop for each entry and save the file

```shell
main() {
  fetch_webmentions | format_output | jq -c '.[]' |
    while IFS= read -r line; do
      save_into_file "$line"
    done

  # ...
}
```

For each file we will see if there existing data, we will need at first merge two of theme and make
sure the merged data have only unique data, so we will compare with `wm-id` with `jq` using
`unique_by(:property_name:)` function and plus `+` operator to merge two arrays

```shell
merge_entries() {
  existing_entries="$1"
  new_entries="$2"

  jq -s '.[0] + .[1] | unique_by(.["wm-id"])' \
    <(echo "$existing_entries") <(echo "$new_entries") |
    sed 's/\([^\\]\)@/\1\\@/g'
}
```

And finally here the final look of the `save_into_file` function

```shell
save_into_file() {
  line="$1"

  target=$(echo "$line" | jq -r '.target')
  properties=$(echo "$line" | jq -c '.properties[]')
  path="src/$target/comments.yaml"

  touch "$path"

  echo "$properties" | while IFS= read -r property; do
    property_name=$(echo "$property" | jq -r ".property")
    new_entries=$(echo "$property" | jq '.entries')

    existing_entries=$(yq -o=json ".$property_name // []" "$path")
    merged_entries=$(merge_entries "$existing_entries" "$new_entries")

    yq -i ".$property_name = $merged_entries" "$path"
  done
}
```

## Conclusion

Now each [blog](/blog) or [thought](/thoughts) have a `comment.yaml` in the same directory,
and i use it as `metadata` with `pandoc` and render it with pandoc template.

```shell
# [!code word:--metadata-file=comments.yaml]

get-webmention-with-jq-and-yq
├── hand-in-hand.jpg
# [!code word:comments.yaml:1]
├── comments.yaml
└── index.md

pandoc --metadata-file=comments.yaml index.md -o index.html
```
Another enhancement we can write `github` workflow just to run [ths
script](https://github.com/22mahmoud/maw.sh/blob/master/bin/webmention) every 12 hours instead to
run it manaully from time time.
