src        := src
output     := dist
pages      := pages
bin        := bin
tmp        := .tmp
extensions := jpeg jpg mp4 gif png txt webp avif

home_md    := $(src)/index.md
md_pages   := $(shell find $(pages) -type f ! -name _home ! -name "*_pagination" \
							| sed 's|$(pages)|$(src)|g' | sed 's|$$|/index.md|')
md_files   := $(shell find $(src) -name "*.md") $(md_pages) $(home_md)
html_files := $(patsubst $(src)/%.md, $(output)/%.html, $(md_files))

build:
	$(MAKE) prepare
	$(MAKE) pages_index
	$(MAKE) html
	$(MAKE) static
	$(MAKE) $(output)/rss.xml
	$(MAKE) $(output)/sitemap.xml

dev:
	@find $(src) filters templates -type f | entr $(MAKE) dist/blog/build-a-blog-with-svelte-and-markdown/index.html

pages_index: $(md_pages) $(home_md)

$(src)/index.md: $(src)/**/* $(pages)/_home
	@$(pages)/_home

$(src)/%/index.md: $(src)/%/**/*.md pages/%
	@$(pages)/$(shell echo $(@) | sed 's/\/index.md//' | xargs basename)

html: $(html_files)

$(output)/rss.xml: $(md_files) $(bin)/rss
	@$(bin)/rss

$(output)/sitemap.xml: $(md_files) $(bin)/sitemap
	@$(bin)/sitemap

default_deps := $(src)/%/index.md templates/* filters/* bin/generate

$(output)/thoughts/index.html: src/thoughts/index.md templates/* filters/* bin/generate  $(wildcard src/thoughts/**/*)
	@bin/generate $< $@

$(output)/%/index.html: $(default_deps) $(src)/%/comments.yaml
	@bin/generate $< $@

$(output)/index.html: $(src)/index.md templates/* filters/* bin/generate
	@bin/generate $< $@

$(output)/%/index.html: $(default_deps)
	@bin/generate $< $@

ext_args := $(shell echo $(extensions) | sed 's/\(\w\+\)/--include="*.\1"/g')
static:
	@rsync -av --update --include="*/" $(ext_args) --exclude="*" $(src)/ $(output)/
	@rsync -av --update --include="*" public/ $(output)/

distclean:
	@rm -vrf $(output) $(md_pages) $(home_md)

clean:
	@rm -vrf $(output) $(tmp) $(md_pages) $(home_md)

prepare:
	mkdir -p $(output)
	mkdir -p $(output)/remote_images
	mkdir -p $(tmp)/images
	touch $(tmp)/images/.nomedia
	npm install

.PHONY: build html static clean dev pages_index prepare distclean
