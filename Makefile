source = src
output = dist
bin = bin

md_files := $(shell find $(source) -name "*.md")
html_files := $(patsubst $(source)/%.md,$(output)/%.html,$(md_files))

thumb := $(bin)/thumb
rss := $(bin)/rss
sitemap := $(bin)/sitemap

install: html static image dist/sitemap.xml dist/rss.xml

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

image:
	@$(thumb)

clean: 
	@rm -vrf $(output)


.PHONY: install html static image clean
