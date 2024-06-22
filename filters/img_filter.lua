local path = require 'pandoc.path'

local function starts_with(str, prefix) return str:sub(1, #prefix) == prefix end

local function get_file_absolute_path(file)
  local current_file = string.gsub(PANDOC_STATE.input_files[1], '([^/]*%.%w+)$', '')
  return ('/' .. path.join { current_file, file }):gsub('^/+', '/')
end

local function remove_file_name(file) return string.gsub(file, '([^/]*%.%w+)$', '') end

local function remove_src_prefix(file) return string.gsub(file, 'src/', '') end

local function slugify_url(url) return url:gsub('[^%w_]', '_') end

local function get_file_extension(file)
  local _, ext = path.split_extension(file)
  return ext
end

local function get_file_name(file)
  local name, _ = path.split_extension(file)
  return name
end

local function is_gif(file) return get_file_extension(file) == '.gif' end

local function get_thumb_path(file)
  local thumb = string.gsub(file, '([^/]*%.%w+)$', 'thumbs/%1')
  return get_file_name(thumb) .. '.webp'
end

local function file_exists(name)
  local f = io.open(name, 'r')
  if f then
    io.close(f)
    return true
  else
    return false
  end
end

local function download_image(url, dest) os.execute('curl -L -o ' .. dest .. ' ' .. url) end

local function get_image_size(file)
  local handle = io.popen('identify -format "%w %h" ' .. file .. ' | head -n1')

  if not handle then return nil, nil end

  local result = handle:read '*a'
  handle:close()

  local width, height = result:match '(%d+) (%d+)'

  return tonumber(width), tonumber(height)
end

local function set_image_size(img, file)
  local width, height = get_image_size(file)
  if width then img.attributes.width = width end
  if height then img.attributes.height = height end
end

local src = 'src'
local dist = 'dist'
local remote_images = 'remote_images/'

local function process_image(input_file, output_file, output_path)
  if file_exists(output_file) then return end

  local tmp_file = string.gsub(output_file, '[/.]', '_')
  tmp_file = '.tmp/images/.' .. tmp_file

  if file_exists(tmp_file) then
    os.execute('mkdir -p ' .. output_path)
    os.execute('cp ' .. tmp_file .. ' ' .. output_file)
    return
  end

  os.execute('mkdir -p ' .. output_path)
  local width, _ = get_image_size(input_file)

  if width <= 768 then
    os.execute('cwebp -q 90 ' .. input_file .. ' -o ' .. output_file)
  else
    os.execute('cwebp -resize 768 0 -q 90 ' .. input_file .. ' -o ' .. output_file)
  end

  os.execute('cp ' .. output_file .. ' ' .. tmp_file)
end

function Image(img)
  img.attributes.loading = 'lazy'

  if starts_with(img.src, 'https://') or starts_with(img.src, 'http://') then
    local slug = slugify_url(img.src)
    local tmp_image = '.tmp/images/' .. slug .. get_file_extension(img.src)
    local dist_image = remote_images .. slug .. get_file_extension(img.src)
    local output_path = dist .. '/' .. remote_images

    if not file_exists(tmp_image) then download_image(img.src, tmp_image) end

    img.src = '/' .. dist_image
    process_image(tmp_image, dist .. '/' .. dist_image, output_path)
    set_image_size(img, dist .. '/' .. dist_image)

    return pandoc.Link(img, img.src)
  end

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

  process_image(input_file, output_file, output_path)
  img.src = thumb
  set_image_size(img, output_file)

  return pandoc.Link(img, absolute_path)
end
