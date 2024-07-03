local u = require 'filters.utils'
local path = require 'pandoc.path'

local src = 'src'
local dist = 'dist'
local tmp = '.tmp'
local remote_images = 'remote_images'
local images = 'images'

local function is_remote_src(file)
  return u.starts_with(file, 'https://') or u.starts_with(file, 'http://')
end

local function get_file_absolute_path(file)
  if not path.is_relative(file) or is_remote_src(file) then return file end

  return path.normalize(
    path.join { '/', u.dirname(PANDOC_STATE.input_files[1]):gsub('src/', ''), file }
  )
end

local function slugify(url)
  local slugified = url:gsub('[^%w_]', '_')
  return slugified
end

local function get_file_extension(file)
  local _, ext = path.split_extension(file)
  return ext
end

local function get_file_name(file)
  local name, _ = path.split_extension(file)
  return name
end

local function is_gif(file)
  local ext = get_file_extension(file)
  return ext == '.gif'
end

local function is_video(file)
  local ext = get_file_extension(file)
  return ext == '.mp4'
end

local function get_thumb_path(file)
  return path.join {
    u.dirname(file),
    'thumbs',
    string.format('%s.webp', get_file_name(u.basename(file))),
  }
end

local function download_image(url, output)
  os.execute(('mkdir -p %s'):format(u.dirname(output)))
  os.execute(('curl -L -o %s %s'):format(output, url))
end

local function get_image_size(file)
  local cmd = is_video(file)
      and 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x %s'
    or 'identify -format "%%w %%h" %s | head -n1'

  local result = u.shell(cmd:format(file))

  local width, height = result:match '(%d+)[%sx](%d+)'

  return tonumber(width), tonumber(height)
end

local function set_image_size(img, file)
  local width, height = get_image_size(file)
  if width then img.attributes.width = width end
  if height then img.attributes.height = height end
end

local function process_image(input, output)
  if u.file_exists(output) then return end

  local output_path = u.dirname(output)
  local tmp_file = path.join { tmp, images, slugify(output) }

  os.execute(('mkdir -p %s'):format(output_path))

  if u.file_exists(tmp_file) then
    os.execute(('cp %s %s'):format(tmp_file, output))
    return
  end

  local width, _ = get_image_size(input)
  local resize_opts = width > 768 and '-resize 768 0' or ''

  os.execute(('cwebp %s -q 90 %s -o %s'):format(resize_opts, input, output))
  os.execute(('mkdir -p %s'):format(u.dirname(tmp_file)))
  os.execute(('cp %s %s'):format(output, tmp_file))
end

local function handle_remote_image(img)
  local slug = slugify(img.src)
  local download_path = path.join { dist, remote_images, slug }

  if not u.file_exists(download_path) then download_image(img.src, download_path) end

  local absolute_url = path.join { '/', remote_images, slug }
  local absolute_thumb = get_thumb_path(absolute_url)

  return absolute_url, absolute_thumb
end

local function get_image(img)
  img.attributes.loading = 'lazy'

  local absolute_url = nil
  local absolute_thumb = nil

  if is_remote_src(img.src) then
    absolute_url, absolute_thumb = handle_remote_image(img)
  else
    absolute_url = get_file_absolute_path(img.src)
    absolute_thumb = get_thumb_path(absolute_url)
  end

  local prefix = (not u.starts_with(absolute_url, '/remote_images') and src or dist)
  local input_file = prefix .. absolute_url
  local output_file = dist .. absolute_thumb

  if is_gif(img.src) or is_video(img.src) then
    set_image_size(img, input_file)
    img.src = absolute_url
    return img
  end

  process_image(input_file, output_file)
  set_image_size(img, output_file)
  img.src = absolute_thumb

  return img, absolute_url, absolute_thumb
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
    Meta = function(meta)
      local function action(value)
        local temp_img = pandoc.Image({}, pandoc.utils.stringify(value))

        local img, absolute_url, absolute_thumb, _ = get_image(temp_img)

        return {
          url = absolute_url,
          thumb = absolute_thumb,
          width = img.attributes.width,
          height = img.attributes.height,
        }
      end

      get_image_meta(meta, action)
      return meta
    end,
  },
  {
    Image = function(original_img)
      local img, absolute_url, _ = get_image(original_img)

      if is_gif(img.src) or is_video(img.src) then return img end

      return pandoc.Link(img, absolute_url)
    end,
  },
  {
    Inline = function(el)
      local function action(value)
        local temp_img = pandoc.Image({}, value)

        local img, absolute_url, absolute_thumb, _ = get_image(temp_img)

        local attrs = ''
        for k, v in pairs(img.attributes) do
          attrs = ('%s %s="%s"'):format(attrs, k, v)
        end

        local img_tag = [[<a href="%s"><img loading="lazy" src="%s" %s /></a>]]

        return img_tag:format(absolute_url, absolute_thumb, attrs)
      end

      return get_image_inline(el, action)
    end,
  },
}
