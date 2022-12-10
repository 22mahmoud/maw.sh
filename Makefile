SOURCE_DIR = src
DEST_DIR = dist
BIN_DIR = bin
MD_FILES := $(shell find $(SOURCE_DIR) -name "*.md")
HTML_FILES := $(patsubst $(SOURCE_DIR)/%.md,$(DEST_DIR)/%.html,$(MD_FILES))
MD_TO_HTML := $(BIN_DIR)/md_to_html
THUMB := $(BIN_DIR)/thumb

all: html static image

html: $(HTML_FILES)

dist/%.html: src/%.md templates/*
	@$(MD_TO_HTML) "$<" "$@"

static:
	cd $(SOURCE_DIR) && find . -type f ! -name "*.md" -print0 | cpio -pdvm0 ../$(DEST_DIR)

image:
	@$(THUMB)

clean: 
	rm -rf $(DEST_DIR)
