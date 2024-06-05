source = src
output = dist
bin = bin
tmp = .tmp
tmp_images = $(tmp)/images
extensions := -iname "*.jpeg" -o -iname "*.jpg" -o  -iname "*.mp4" -o  -iname "*.gif" -o \
							-iname "*.png" -o  -iname "*.txt" -o  -iname "*.webp" -o  -iname "*.avif"

md_files := $(shell find $(source) -name "*.md")
thoughts_md_files := $(shell find $(source)/thougts -name "*.md" ! -wholename $(source)/thoughts/index.md)
games_md_files := $(shell find $(source)/games -name "*.md" ! -wholename $(source)/games/index.md)
html_files := $(patsubst $(source)/%.md,$(output)/%.html,$(md_files))

thumb := $(bin)/thumb
rss := $(bin)/rss
sitemap := $(bin)/sitemap

install: preinstall prepare html static dist/sitemap.xml dist/rss.xml

dev:
	find src filters templates -type f | entr make install

preinstall:
	rm -rf node_modules && npm install

html: $(html_files)

src/games/index.md: $(games_md_files)
	@$(bin)/game_index

src/thoughts/index.md: $(thoughts_md_files)
	@$(bin)/thoughts_index

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
	@rm -vrf $(output) $(tmp)

prepare:
	@mkdir -p $(output)
	@mkdir -p $(tmp_images)
	@touch $(tmp_images)/.nomedia

.PHONY: install html static clean dev preinstall
