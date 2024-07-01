src        := src
output     := dist
pages      := pages
bin        := bin
tmp        := .tmp
extensions := jpeg jpg mp4 gif png txt webp avif

md_files   := $(shell find $(src) -name "*.md" ! -path $(src)/index.md) 
html_files := $(patsubst $(src)/%.md, $(output)/%.html, $(md_files))

build:
	$(MAKE) prepare
	$(MAKE) html
	$(MAKE) static
	$(MAKE) $(output)/rss.xml
	$(MAKE) $(output)/sitemap.xml

dev:
	@find $(src) filters templates -type f | entr $(MAKE) dist/blog/build-a-blog-with-svelte-and-markdown/index.html

html: $(html_files) $(output)/index.html

$(output)/rss.xml: $(md_files) $(bin)/rss
	@$(bin)/rss

$(output)/sitemap.xml: $(md_files) $(bin)/sitemap
	@$(bin)/sitemap

default_deps := $(src)/%/index.md templates/* filters/* bin/generate $(wildcard src/%/**/*)

$(output)/index.html: src/index.md templates/* filters/* bin/generate $(md_files)
	@bin/generate $< $@

$(output)/%/index.html: $(default_deps) $(src)/%/comments.yaml $(wildcard src/%/**/*)
	@bin/generate $< $@

$(output)/%/index.html: $(default_deps) $(wildcard src/%/**/*)
	@bin/generate $< $@

ext_args := $(shell echo $(extensions) | sed 's/\(\w\+\)/--include="*.\1"/g')
static:
	@rsync -av --update --include="*/" $(ext_args) --exclude="*" $(src)/ $(output)/
	@rsync -av --update --include="*" public/ $(output)/

distclean:
	@rm -vrf $(output)

clean:
	@rm -vrf $(output) $(tmp)

prepare:
	mkdir -p $(output)
	mkdir -p $(output)/remote_images
	mkdir -p $(tmp)/images
	touch $(tmp)/images/.nomedia
	npm install

.PHONY: build html static clean dev prepare distclean
