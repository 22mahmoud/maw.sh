local path = require("pandoc.path")

function Image(img)
	local src = img.src

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

function RawInline(raw)
	if raw.format == "html" and raw.text:match("^<img") then
		print(raw.t)
	end

	return raw
end
