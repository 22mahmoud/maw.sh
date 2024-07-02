---
slug: uninstall-all-neovim-plugins
title-prefix: Uninstall all neovim plugins
date: 2022-12-02T00:00+02:00
description: This Article about using neovim on a Unix way.
keywords: linux, neovim, vim
category: vim
featured-image: /blog/uninstall-all-neovim-plugins/matrix.jpg
post: true
---

![the matrix movie scene](/blog/uninstall-all-neovim-plugins/matrix.jpg)

As a developer, you need a robust environment that fits your needs to develop,
compile, debug, build, and so on. So, you have now two pills to choose one of
them. And most probably if you read this article you have already chosen the
red one. But unfortunately, Neovim plugins does not give you the full control of
the experience.

## Why vim/neovim and not vscode/intellij?

I choose vim/neovim because I need a "just" code editor, and also it can be
easily leverage my tools capabilities on UNIX way, and you can read more on
this article [Unix as an IDE](https://blog.sanctum.geek.nz/series/unix-as-ide/),
but the all-in-solutions, like an IDE, is not the right tool for code editing,
it came with a lot of features and defaults that you in most cases I don't need
it, or I have to learn how to use them according to that IDE.

## So, Why neovim not vim?

I used to use vim before, but I need an editor that more focused natively on
"code", Not just a plain text, So neovim is a good choice for developers to
enhance the coding experience by using lsp, and treesitter.

## immature plugin ecosystem

To be honest, one of the problems on the neovim community is nonsense plugins
that just a replicate vim plugins or plugins that do what we should do in the
terminals but using lua as plugin on neovim. Also, It used at the beginning to be
missing the help documentation but now I believe it gets better, so it is nice.

Also, what they called "neovim distributions" which another layer of complexity
that tight your use by using the author setting file.

## How to escape, and use neovim on unix way

What I've done is first delete all my plugins, and start with a clean
`init.lua` file with simple configuration, and gradually see what I'm really
miss and add it into my config.

If the feature that I need can be easily implemented with neovim config only
I'll go to this direction, but if not I'll search for small and well-written and
well-documented plugin and also if it has a lot of features, I'll go first to
copy-paste code into my neovim config and start tweaking it.

## Examples time

#### - search/browse files:

for the codebase navigation I'll use the vim `find`, `buffers` commands but
instead of using `vim.opt.path:append "*"` which leads to hang the command on
projects that's have for example `node_module` I will use the local `.nvimrc` on
each project to extend my config

```lua
-- Load .nvimrc manually
local local_vimrc = vim.fn.getcwd() .. '/.nvimrc.lua'
if vim.loop.fs_stat(local_vimrc) then
  local source = vim.secure.read(local_vimrc)
  if not source then
    return
  end

  vim.cmd(string.format('so %s', local_vimrc))
end
```

so on the project root directory I can create a new file `.nvimrc.lua` and add
this line e.g:

```lua
vim.opt.path:append({ "src/**", })
-- and any config that I need for this project
```

And for search on the files there is a vim `grep` command with some modification
that makes it work more performant by using [ripgrep](/blog/my-terminal-became-more-rusty/#ripgrep)

```lua
-- better grip with 'rg'
if vim.fn.executable 'rg' == 1 then
  o.grepprg = [[rg --hidden --smart-case --vimgrep]]
  o.grepformat = { '%f:%l:%c:%m' }
end
```

and the nice about grep that the result now on your quickfix, so you can easily
navigate between them, and do any operation that you want.

![a screenshot of neovim with quickfix opend](/blog/uninstall-all-neovim-plugins/quickfix-vim-screenshot.jpg)

And here is my mapping, it may be useful, and here is the [utils](https://github.com/22mahmoud/nvim/blob/master/lua/ma/utils.lua) used in the
snippets below:

```lua
-- navigation & find & search
G.nnoremap('<leader>p', ':find<space>', { silent = false })
G.nnoremap('<leader>rg', ':silent grep ""<left>', { silent = false })
G.nnoremap('<leader>gw', ':silent grep <C-R>=expand("<cword>")<CR><CR>')

-- buffers
G.nnoremap('<leader>bn', ':bn<cr>')
G.nnoremap('<leader>bp', ':bp<cr>')
G.nnoremap('<leader>bl', ':ls t<cr>:b<space>', { silent = false })
G.nnoremap('<leader>bd', ':bd!<cr>')

-- quick list
G.nnoremap('<leader>qn', ':cn<cr>')
G.nnoremap('<leader>qp', ':cp<cr>')
G.nnoremap('<leader>ql', G.toggle_qf, { nowait = false })
G.nnoremap('<leader>qq', ':cex []<cr>')
```

### - code completion

I'm kinda person that doesn't like a destruction while typing, so fuzzy
finder, and auto pop-up menus not a good solution for me. I prefer to go also
with the native [ins-compilation](https://neovim.io/doc/user/insert.html#ins-completion) and use completion menu on demand by a specific
category.

### - statusline/winbar

For this one I need it very simple so I write it by myself after I submit this
[post](https://old.reddit.com/r/neovim/comments/q3jur8/please_share_your_statusline_config_lua_no/)
on `/r/neovim` sub-reddit and get a lot of inspiration.

### - Git

Why should I integrate git inside neovim! I use git on my terminal inside tmux
session using some helpful commands that fits on my workflow. and that is on of
them:

```sh
# `-p` will open interactive mode to add/reset based on the hunks
git add -p
git reset -p
```

![a screenshot of `git add -p` command](/blog/uninstall-all-neovim-plugins/hunks-screenshot.jpg)

### - Neovim goodies (lsp/treesitter)

This is the part that I'm really have to use official plugins so let's install
packer... Or wait a minute, why not just use the native solution.

there is a [vim packages](https://neovim.io/doc/user/repeat.html#packages) is a
directory you can download your plugins inside it and just it nothing more to
do.

```sh
cd ~/.local/share/nvim
git init .
git submodule init
mkdir site/pack/plugins/opt/
git submodule add --depth 1 https://github.com/neovim/nvim-lspconfig site/pack/plugins/opt/nvim-lspconfig
```

and I wrote a wrapper on `lua` to make the process easy and similar to the
package managers [check it out](https://github.com/22mahmoud/nvim/blob/master/lua/ma/plugins.lua)

### - Theming

I just use [nvim-base16](https://github.com/RRethy/nvim-base16) plugin to fit
my base16 theme system.

## conclusion

After adding all my needs I find out that there was many plugins on my config
that does not help me or not fit on my workflow. e.g: I do not use snippets,
file explorer, fuzzy finders.
