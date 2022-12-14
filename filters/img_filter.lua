local path = require("pandoc.path")

function Image(img)
	local src = img.src
	img.attributes.loading = "lazy"

	local _, ext = path.split_extension(src)
	if ext == ".gif" then
		return img
	end

	-- Add the 'thumbs/' prefix to the image filename
	img.src = string.gsub(img.src, "([^/]*%.%w+)$", "thumbs/%1")

	-- Split the image filename and file extension
	local filename = path.split_extension(img.src)

	-- Set the file extension to '.webp'
	img.src = filename .. ".webp"

	-- Wrap the image in an anchor tag
	local link = pandoc.Link(img, src)

	-- Return the modified image
	return link
end
