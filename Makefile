src        := src
output     := dist
pages      := pages
bin        := bin
tmp        := .tmp
extensions := jpeg jpg mp4 gif png txt webp avif
excludes   := $(src)/rss/index.md $(src)/rss-thoughts/index.md $(src)/index.md

excludes_args  := $(shell echo $(excludes) | sed 's/[^ ]*/! -path &/g')
md_files       := $(shell find $(src) -name "*.md" $(excludes_args))
html_files     := $(patsubst $(src)/%.md, $(output)/%.html, $(md_files))

blog_files      := $(shell find $(src)/blog -name "*.md" ! -path src/blog/index.md)
thoughts_files  := $(shell find $(src)/thoughts -name "*.md" ! -path src/thoughts/index.md)

build: static $(output)/rss-thoughts.xml $(output)/rss.xml $(output)/sitemap.xml

dev:
	@find $(src) filters templates -type f | entr $(MAKE) dist/blog/build-a-blog-with-svelte-and-markdown/index.html

prepare: static
	@mkdir -pv $(output)
	@mkdir -pv $(output)/remote_images
	@mkdir -pv $(tmp)/images
	touch $(tmp)/images/.nomedia

html: prepare $(html_files) $(output)/index.html

$(output)/rss.xml: $(blog_files) prepare templates/rss.xml
	@$(bin)/generate $@

$(output)/rss-thoughts.xml: $(thoughts_files) prepare templates/rss.xml
	@$(bin)/generate $@

$(output)/sitemap.xml: html $(md_files) prepare $(bin)/sitemap
	@$(bin)/sitemap

$(output)/index.html: $(src)/index.md $(md_files) prepare templates/* filters/* bin/generate
	@$(bin)/generate $@

$(output)/%/index.html: $(src)/%/* prepare templates/* filters/* bin/generate
	@$(bin)/generate $@

ext_args := $(shell echo $(extensions) | sed 's/\(\w\+\)/--include="*.\1"/g')
static:
	@rsync -av --update --include="*/" $(ext_args) --exclude="*" $(src)/ $(output)/
	@rsync -av --update --include="*" public/ $(output)/
	@rsync -av --update --include="*" assets/ $(output)/

distclean:
	@rm -vrf $(output)

clean:
	@rm -vrf $(output) $(tmp)

.PHONY: build html static clean dev prepare distclean last_update
