source = src
output = dist
bin = bin
tmp = .tmp
tmp_images = $(tmp)/images
extensions := -iname "*.jpeg" -o -iname "*.jpg" -o  -iname "*.mp4" -o  -iname "*.gif" -o \
							-iname "*.png" -o  -iname "*.txt" -o  -iname "*.webp" -o  -iname "*.avif"

thoughts_index := $(source)/thoughts/index.md
games_index := $(source)/games/index.md
blog_index := $(source)/blog/index.md

md_files := $(shell find $(source) -name "*.md") $(thoughts_index) $(games_index) $(blog_index)
html_files := $(patsubst $(source)/%.md,$(output)/%.html,$(md_files))
thoughts_md_files := $(shell find $(source)/thoughts -name "*.md" ! -wholename $(thoughts_index))
games_md_files := $(shell find $(source)/games -name "*.md" ! -wholename $(games_index))
blog_md_files := $(shell find $(source)/games -name "*.md" ! -wholename $(blog_index))

thumb := $(bin)/thumb
rss := $(bin)/rss
sitemap := $(bin)/sitemap

install: preinstall $(games_index) $(thoughts_index) $(blog_index) prepare html static dist/sitemap.xml dist/rss.xml

dev:
	find src filters templates -type f | entr make install

preinstall:
	npm install

$(games_index): $(games_md_files)
	@$(bin)/game_index

$(thoughts_index): $(thoughts_md_files)
	@$(bin)/thoughts_index

$(blog_index): $(blog_md_files)
	@$(bin)/blog_index

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
	@mkdir -p $(tmp_images)
	@touch $(tmp_images)/.nomedia

.PHONY: install html static clean dev preinstall
