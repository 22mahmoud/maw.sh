---
slug: 'my-terminal-became-more-rusty'
title: 'My terminal became more Rusty 🦀'
date: '2020-08-21'
author: 'Mahmoud Ashraf'
description: 'CLI tools written in rust make my terminal fast and productive'
cover: './cover.jpg'
categories:
  - 'rust'
  - 'cli'
keywords:
  - 'rust'
  - 'cli'
  - 'linux'
  - 'terminal'
---

<img 
  src="./cover.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./cover.jpg?size=320 320w, ./cover.jpg?size=640 640w, 
    ./cover.jpg?size=960 960w, ./cover.jpg?size=1200 1200w, ./cover.jpg?size=1800 1800w, ./cover.jpg?size=2400 2400w"  
  alt="big crap attack the city">

As a Software-Engineer I spent most of the time inside my terminal, So
I need for that a fast terminal with  fast tools to speed up my productivity.

The tools written in rust help me to achieve that. let's see in this article
those tools.

[//]: # "/* cspell:disable */"
> ### tl;dr
> - [alacritty](https://github.com/alacritty/alacritty)  A cross-platform, GPU-accelerated terminal emulator
> - [starship](https://github.com/starship/starship) 🌌 The minimal, blazing-fast, and infinitely customizable prompt for any shell!
> - [exa](https://github.com/ogham/exa) A modern version of ‘ls’.
> - [bat](https://github.com/sharkdp/bat) A cat(1) clone with wings.
> - [delta](https://github.com/dandavison/delta) A viewer for git and diff output
> - [zoxide](https://github.com/ajeetdsouza/zoxide) A faster way to navigate your filesystem
> - [ripgrep](https://github.com/burntsushi/ripgrep) ripgrep recursively searches directories for a regex pattern
> - [fd](https://github.com/sharkdp/fd) A simple, fast and user-friendly alternative to 'find'
> - [bottom](https://github.com/clementtsang/bottom) Yet another cross-platform graphical process/system monitor.
> - [tldr](https://github.com/tldr-pages/tldr) 📚 Collaborative cheatsheets for console commands
> - [spotify-tui](https://github.com/rigellute/spotify-tui) Spotify for the terminal written in Rust 🚀
> - [gitui](https://github.com/extrawurst/gitui) Blazing 💥 fast terminal-ui for git written in rust 🦀
[//]: # "/* cspell:enable */"

### Alacritty

Let's start our list with alacritty terminal is one of the fastest terminals 
because of using GPU for rendering, and it is a cross-platform terminal.

You can customize your own configuration like color scheme, fonts, opacity, and key mapping.

Alacritty doesn't come with ligature support but you can use 
this [fork](https://github.com/zenixls2/alacritty/tree/ligature). or if 
you are using Arch you can install it from [aur](https://aur.archlinux.org/packages/alacritty-ligatures/)

<img 
  src="./alacritty.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./alacritty.jpg?size=320 320w, ./alacritty.jpg?size=640 640w, 
    ./alacritty.jpg?size=960 960w, ./alacritty.jpg?size=1200 1200w, ./alacritty.jpg?size=1800 1800w, ./alacritty.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of the terminal showing alacritty ligatures">

---

### Starship

I used to use zsh + powerlevel9k as my prompt and even when I migrate to powerlevel10k, I still
notice a delay when open new shell. But with starship it's start instantly.

You can use it with any shell bash, zsh, fish and even powerShell.

The screenshot below showing the result of my customized configuration.

<img 
  src="./starship.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./starship.jpg?size=320 320w, ./starship.jpg?size=640 640w, 
    ./starship.jpg?size=960 960w, ./starship.jpg?size=1200 1200w, ./starship.jpg?size=1800 1800w, ./starship.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of starship prompt">

---

### Exa

exa is an implementation of `ls` command but with colors and icons and it renders very fast.

I'm using exa as replacer for ls command by making an alias.

```sh
if [ "$(command -v exa)" ]; then
    unalias -m 'll'
    unalias -m 'l'
    unalias -m 'la'
    unalias -m 'ls'
    alias ls='exa -G  --color auto --icons -a -s type'
    alias ll='exa -l --color always --icons -a -s type'
fi
```

the result of my `ls` and `ll` commands.

<img 
  src="./exa.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./exa.jpg?size=320 320w, ./exa.jpg?size=640 640w, 
    ./exa.jpg?size=960 960w, ./exa.jpg?size=1200 1200w, ./exa.jpg?size=1800 1800w, ./exa.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of exa result">

---

### Bat

Bat is an implementation for `cat` command but with syntax highlighted.

Also I make an alias for this command with nord theme.

```sh
if [ "$(command -v bat)" ]; then
  unalias -m 'cat'
  alias cat='bat -pp --theme="Nord"'
fi
```

<img 
  src="./bat.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./bat.jpg?size=320 320w, ./bat.jpg?size=640 640w, 
    ./bat.jpg?size=960 960w, ./bat.jpg?size=1200 1200w, ./bat.jpg?size=1800 1800w, ./bat.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of bat">

---

### Delta

delta enhance your git diff output by adding some cool features like syntax highlighting,
line numbering, and side-by-side view.

to make delta works in your `.gitconfig` file add:

```yaml
[core]
  pager = delta
[interactive]
  diffFilter = delta --color-only
[delta]
  side-by-side = true
  line-numbers-left-format = ""
  line-numbers-right-format = "│ "
  syntax-theme = Nord
```

we set `delta` as the default pager for git commands output and enable side-by-side 
feature and set a theme for Nord, You can choose your preferred theme  run and choose one.

```sh
delta --list-syntax-themes
```

<img 
  src="./delta.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./delta.jpg?size=320 320w, ./delta.jpg?size=640 640w, 
    ./delta.jpg?size=960 960w, ./delta.jpg?size=1200 1200w, ./delta.jpg?size=1800 1800w, ./delta.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of delta">

---

### Zoxide

I don't use any file explorer, I just use `cd` command to navigate between the files and `ls` commands.

I have a `projects` directory on my home folder if I wanna navigate to a project of those projects.
I will write

```sh
cd ~/projects/mahmoudashraf.dev
```

instead I will write 

```sh
z ~/projects/mahmoudashraf.dev
```

just to the first time and if I wanna navigate again to this directory from anywhere
just write 

```sh
z mah
```

---

### Ripgrep

It is a  cross-platform command line searches your directory for a regex pattern. 

I recommend you read this article [ripgrep is faster than {grep, ag, git grep, ucg, pt, sift}
](https://blog.burntsushi.net/ripgrep/).

some commands that i'm using

```sh
# search on javascript files for specific regex
rg tjs "import React"

rg "\.content" -g "*.pug"

# you can also search and replace with regex as sed command
rg fast README.md --replace FAST
```
<img 
  src="./ripgrep.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./ripgrep.jpg?size=320 320w, ./ripgrep.jpg?size=640 640w, 
    ./ripgrep.jpg?size=960 960w, ./ripgrep.jpg?size=1200 1200w, ./ripgrep.jpg?size=1800 1800w, ./ripgrep.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of ripgrep">

---

### Fd

the friendly version of `find` command, and faster.

It's by default ignore `.gitignore` file

in this tutorial I have some screenshots in `png` format to convert them all to `jpg`:

```sh
fd -e png -x convert {} {.}.jpg
```

To delete files

```sh
fd -H '^\.DS_Store$' -tf -X rm
```

---

### bottom

In this time not `top` 😀 it is `bottom`

it's a cross-platform system monitor. 

<img 
  src="./bottom.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./bottom.jpg?size=320 320w, ./bottom.jpg?size=640 640w, 
    ./bottom.jpg?size=960 960w, ./bottom.jpg?size=1200 1200w, ./bottom.jpg?size=1800 1800w, ./bottom.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of bottom">

---


### Tldr

tldr is a cheatsheets for CLIs, instead of read the whole `man`.

<img 
  src="./tldr.jpg" 
  sizes='(min-width: 1024px) 1024px, 100vw'
  srcSet="./tldr.jpg?size=320 320w, ./tldr.jpg?size=640 640w, 
    ./tldr.jpg?size=960 960w, ./tldr.jpg?size=1200 1200w, ./tldr.jpg?size=1800 1800w, ./tldr.jpg?size=2400 2400w"  
  loading="lazy"
  alt="screenshot of tldr">

---

### More Tools?

- for who want lightweight alternative for github client you can use `spotify-tui`.
- also if you prefer an UI interface  for git check `gitui`.

and there is a ton of CLIs and tools written in rust you can check 
[lib.rs/command-line-utilities](https://lib.rs/command-line-utilities)




