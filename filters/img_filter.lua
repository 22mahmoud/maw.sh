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

local function handle_remote_image(img)
  local slug = slugify_url(img.src)
  local tmp_image = '.tmp/images/' .. slug .. get_file_extension(img.src)
  local input_file = remote_images .. slug .. get_file_extension(img.src)
  local thumb = get_thumb_path(input_file)
  local output_file = dist .. '/' .. thumb
  local output_path = dist .. '/' .. remove_file_name(thumb)

  if not file_exists(tmp_image) then download_image(img.src, tmp_image) end

  process_image(tmp_image, output_file, output_path)
  img.attributes.original_src = '/' .. input_file
  img.src = '/' .. thumb
  set_image_size(img, output_file)

  return img
end

local function get_image(img)
  img.attributes.loading = 'lazy'

  if starts_with(img.src, 'https://') or starts_with(img.src, 'http://') then
    handle_remote_image(img)

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

local function get_image_meta(metadata, action)
  if type(metadata) == 'table' then
    for key, value in pairs(metadata) do
      if key == 'photo' then
        metadata[key] = action(value)
      else
        get_image_meta(value, action)
      end
    end
  end
end

local function get_image_inline(el, action)
  if el.format == 'html' then
    -- Find and process <img> tags
    local html_content = el.text
    local match = html_content:gmatch '<img.*/>'

    for img_tag in match do
      local value = img_tag:match 'src="([^"]+)"'
      el.text = action(value)
    end

    return el
  end
end

return {
  {
    Image = get_image,
  },
  {
    Meta = function(meta)
      local function action(value)
        local img = pandoc.Image({ pandoc.Str 'placeholder image' }, pandoc.utils.stringify(value))

        handle_remote_image(img)

        return {
          url = img.attributes.original_src,
          thumb = img.src,
          width = img.attributes.width,
          height = img.attributes.height,
        }
      end

      get_image_meta(meta, action)
      return meta
    end,
  },
  {
    Inline = function(el)
      local function action(value)
        local img = pandoc.Image({ pandoc.Str 'placeholder image' }, value)

        handle_remote_image(img)

        local src = img.attributes.original_src
        local thumb = img.src
        local attr = img.attributes

        local img_tag = '<a href="' .. src .. '"><img loading="lazy" src="' .. thumb .. '"'

        for k, v in pairs(attr) do
          img_tag = img_tag .. ' ' .. k .. '="' .. v .. '"'
        end

        img_tag = img_tag .. ' /></a>'

        return img_tag
      end

      return get_image_inline(el, action)
    end,
  },
}
