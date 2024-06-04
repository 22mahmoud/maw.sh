source = src
output = dist
bin = bin
tmp = .tmp
tmp_images = $(tmp)/images
extensions := -iname "*.jpeg" -o -iname "*.jpg" -o  -iname "*.mp4" -o  -iname "*.gif" -o \
							-iname "*.png" -o  -iname "*.txt" -o  -iname "*.webp" -o  -iname "*.avif"

md_files := $(shell find $(source) -name "*.md")
html_files := $(patsubst $(source)/%.md,$(output)/%.html,$(md_files))

thumb := $(bin)/thumb
rss := $(bin)/rss
sitemap := $(bin)/sitemap

install: prepare thoughts_index game_index html static dist/sitemap.xml dist/rss.xml

dev:
	find src filters templates -type f | entr make install

html: $(html_files)

game_index:
	@$(bin)/game_index

thoughts_index:
	@$(bin)/thoughts_index

dist/rss.xml: $(md_files) $(rss)
	@$(rss)

dist/sitemap.xml: $(md_files) $(sitemap)
	@$(sitemap)

dist/%.html: src/%.md templates/* $(MD_TO_HTML)
	@mkdir -p $(@D)
	@pandoc -d pandoc.yaml $< -o $@
	@echo "[html generated]:" $@

static:
	find $(source) -type f \( $(extensions) \)  -print0 | cpio -pdvm0 $(output)
	cp -r public/* $(output)

clean: 
	@rm -vrf $(output)

prepare:
	@mkdir -p $(output)
	@mkdir -p $(tmp_images)
	@touch $(tmp_images)/.nomedia

.PHONY: install html static clean dev game_index thoughts_index
