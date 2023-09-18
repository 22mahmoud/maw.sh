source = src
output = dist
bin = bin
tmp = .tmp
tmp_images = $(tmp)/images

md_files := $(shell find $(source) -name "*.md")
html_files := $(patsubst $(source)/%.md,$(output)/%.html,$(md_files))

thumb := $(bin)/thumb
rss := $(bin)/rss
sitemap := $(bin)/sitemap

install: prepare html static dist/sitemap.xml dist/rss.xml

dev:
	find src filters templates -type f | entr make install

html: $(html_files)

dist/rss.xml: $(md_files) $(rss)
	@$(rss)

dist/sitemap.xml: $(md_files) $(sitemap)
	@$(sitemap)

dist/%.html: src/%.md templates/* $(MD_TO_HTML)
	@mkdir -p $(@D)
	@pandoc -d pandoc.yaml $< -o $@
	@echo "[html generated]:" $@

static:
	cd $(source) && find . -type f ! -name "*.md" -print0 | cpio -pdvm0 ../$(output)
	cp -r public/* $(output)

clean: 
	@rm -vrf $(output)

prepare:
	@mkdir -p $(output)
	@mkdir -p $(tmp_images)
	@touch $(tmp_images)/.nomedia

.PHONY: install html static clean dev
