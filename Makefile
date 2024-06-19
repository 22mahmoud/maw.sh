source = src
output = dist
pages = pages
bin = bin
tmp = .tmp
extensions := -iname "*.jpeg" -o -iname "*.jpg" -o  -iname "*.mp4" -o  -iname "*.gif" -o \
							-iname "*.png" -o  -iname "*.txt" -o  -iname "*.webp" -o  -iname "*.avif"

index_files := $(shell find $(source) -maxdepth 1 -type d ! -path $(source) -exec basename {} \;)

md_files := $(shell find $(source) -name "*.md")
html_files := $(patsubst $(source)/%.md,$(output)/%.html,$(md_files))

thumb := $(bin)/thumb
rss := $(bin)/rss
sitemap := $(bin)/sitemap

install: preinstall prepare pages_index html static dist/sitemap.xml dist/rss.xml

dev:
	find src filters templates -type f | entr make install

preinstall:
	npm install

pages_index: $(index_files)

$(index_files):
	@if [ -f $(pages)/$(@) ]; then $(pages)/$(@); fi

html: $(html_files)

dist/rss.xml: $(md_files) $(rss)
	@$(rss)

dist/sitemap.xml: $(md_files) $(sitemap)
	@$(sitemap)

dist/%.html: src/%.md templates/* filters/*
	@mkdir -p $(@D)
	@pandoc -d pandoc.yaml $< -o $@
	@echo "[html generated]:" $@

static:
	cd $(source) && find . -type f \( $(extensions) \)  -print0 | cpio -pdmu0 ../$(output)
	cp -r public/* $(output)

clean: 
	@rm -vrf $(output) $(tmp) $(games_index) $(thoughts_index) $(blog_index)

prepare:
	@mkdir -p $(output)
	@mkdir -p $(tmp)/images
	@touch $(tmp)/images/.nomedia

.PHONY: install html static clean dev preinstall pages_index $(index_files)
