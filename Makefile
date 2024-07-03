src        := src
output     := dist
pages      := pages
bin        := bin
tmp        := .tmp
extensions := jpeg jpg mp4 gif png txt webp avif

md_files   := $(shell find $(src) -name "*.md" ! -path $(src)/index.md)
html_files := $(patsubst $(src)/%.md, $(output)/%.html, $(md_files))

build:
	npm install
	$(MAKE) static $(output)/rss-thoughts.xml $(output)/rss.xml $(output)/sitemap.xml

dev:
	@find $(src) filters templates -type f | entr $(MAKE) dist/blog/build-a-blog-with-svelte-and-markdown/index.html

prepare:
	mkdir -p $(output)
	mkdir -p $(output)/remote_images
	mkdir -p $(tmp)/images
	touch $(tmp)/images/.nomedia

html: prepare $(html_files) $(output)/index.html

$(output)/rss.xml: html $(md_files) $(bin)/rss
	@$(bin)/rss

$(output)/rss-thoughts.xml: html $(md_files) $(bin)/rss-thoughts
	@$(bin)/rss-thoughts

$(output)/sitemap.xml: html $(md_files) $(bin)/sitemap
	@$(bin)/sitemap

$(output)/index.html: $(src)/index.md $(md_files) templates/* filters/* bin/generate
	@bin/generate $@

$(output)/%/index.html: $(src)/%/* templates/* filters/* bin/generate
	@bin/generate $@

ext_args := $(shell echo $(extensions) | sed 's/\(\w\+\)/--include="*.\1"/g')
static: html
	@rsync -av --update --include="*/" $(ext_args) --exclude="*" $(src)/ $(output)/
	@rsync -av --update --include="*" public/ $(output)/

distclean:
	@rm -vrf $(output)

clean:
	@rm -vrf $(output) $(tmp)

.PHONY: build html static clean dev prepare distclean last_update
