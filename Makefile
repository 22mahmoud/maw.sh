src        := src
output     := dist
pages      := pages
bin        := bin
tmp        := .tmp
extensions := jpeg jpg mp4 gif png txt webp avif

md_pages   := $(shell find $(pages) -type f | sed 's|$(pages)|$(src)|g' | sed 's|$$|/index.md|')
md_files   := $(shell find $(src) -name "*.md") $(md_pages)
html_files := $(patsubst $(src)/%.md, $(output)/%.html, $(md_files))

build: prepare pages_index html static $(output)/sitemap.xml $(output)/rss.xml

dev:
	@find $(src) filters templates -type f | entr $(MAKE) dist/blog/build-a-blog-with-svelte-and-markdown/index.html

pages_index: $(md_pages)

$(src)/%/index.md: $(src)/%/**/*.md pages/%
	@$(pages)/$(shell echo $(@) | sed 's/\/index.md//' | xargs basename)

html: $(html_files)

$(output)/rss.xml: $(md_files) $(bin)/rss
	@$(bin)/rss

$(output)/sitemap.xml: $(md_files) $(bin)/sitemap
	@$(bin)/sitemap

default_deps := $(src)/%/index.md templates/* filters/* bin/generate

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

clean:
	@rm -vrf $(output) $(tmp) $(md_pages)

prepare:
	mkdir -p $(output)
	mkdir -p $(output)/remote_images
	mkdir -p $(tmp)/images
	touch $(tmp)/images/.nomedia
	npm install

.PHONY: build html static clean dev pages_index
