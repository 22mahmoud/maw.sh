SOURCE_DIR = src
DEST_DIR = dist
BIN_DIR = bin
MD_FILES := $(shell find $(SOURCE_DIR) -name "*.md")
HTML_FILES := $(patsubst $(SOURCE_DIR)/%.md,$(DEST_DIR)/%.html,$(MD_FILES))
MD_TO_HTML := $(BIN_DIR)/md_to_html
THUMB := $(BIN_DIR)/thumb
RSS := $(BIN_DIR)/rss
SITEMAP := $(BIN_DIR)/sitemap

all: html static image rss sitemap

html: $(HTML_FILES)

rss: $(DEST_DIR)/rss.xml

sitemap: $(DEST_DIR)/sitemap.xml

dist/%.html: src/%.md templates/*
	@$(MD_TO_HTML) "$<" "$@"

static:
	cd $(SOURCE_DIR) && find . -type f ! -name "*.md" -print0 | cpio -pdvm0 ../$(DEST_DIR)

$(DEST_DIR)/rss.xml: $(MD_FILES)
	$(RSS)

$(DEST_DIR)/sitemap.xml: $(MD_FILES)
	$(SITEMAP)

image:
	@$(THUMB)

clean: 
	rm -rf $(DEST_DIR)
