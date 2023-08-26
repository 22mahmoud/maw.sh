local path = require("pandoc.path")

local function get_file_absolute_path(file)
	local current_file = string.gsub(PANDOC_STATE.input_files[1], "([^/]*%.%w+)$", "")
	return "/" .. path.join({ current_file, file })
end

local remove_file_name = function(file)
	return string.gsub(file, "([^/]*%.%w+)$", "")
end

local remove_src_prefix = function(file)
	return string.gsub(file, "src/", "")
end

local function get_file_extension(file)
	local _, ext = path.split_extension(file)
	return ext
end

local get_file_name = function(file)
	local name, _ = path.split_extension(file)
	return name
end

local is_gif = function(file)
	local ext = get_file_extension(file)
	return ext == ".gif"
end
local function get_thumb_path(file)
	-- add thumbs/ to the path
	local thumb = string.gsub(file, "([^/]*%.%w+)$", "thumbs/%1")

	-- change extension to .webp
	return get_file_name(thumb) .. ".webp"
end

local set_image_size = function(img, path)
	local handle = io.popen('identify -format "%w %h\n" ' .. path .. " | head -n1")
	local result = handle:read("*a")
	handle:close()

	local width, height = result:match("(%d+) (%d+)")

	if width then
		img.attributes.width = width
	end

	if height then
		img.attributes.height = height
	end
end

local src = "src"
local dist = "dist"

function Image(img)
	img.attributes.loading = "lazy"

	local absolute_path = remove_src_prefix(get_file_absolute_path(img.src))
	local thumb = get_thumb_path(absolute_path)

	local input_file = src .. absolute_path
	local output_file = dist .. thumb
	local output_path = dist .. remove_file_name(thumb)

	if is_gif(img.src) then
		set_image_size(img, input_file)
		img.src = absolute_path
		return img
	end

	os.execute("mkdir -p " .. output_path)
	os.execute("cwebp -resize 640 0 -q 80 " .. input_file .. " -o " .. output_file)

	img.src = thumb

	set_image_size(img, output_file)

	-- Wrap the image in an anchor tag
	local link = pandoc.Link(img, absolute_path)

	-- Return the modified image
	return link
end
