local u = require 'filters.utils'
local path = require 'pandoc.path'

local src = 'src'
local dist = 'dist'
local tmp = '.tmp'
local remote_images = 'remote_images'
local images = 'images'
local current_file = PANDOC_STATE.input_files[1]

local function is_remote_src(file)
  return u.starts_with(file, 'https://') or u.starts_with(file, 'http://')
end

local function get_file_absolute_path(file)
  if not path.is_relative(file) or is_remote_src(file) then return file end

  return path.normalize(path.join { '/', u.dirname(current_file):gsub('src/', ''), file })
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

local function is_gif(file) return get_file_extension(file) == '.gif' end

local function is_video(file) return get_file_extension(file) == '.mp4' end

local function get_thumb_path(file)
  return path.join { u.dirname(file), 'thumbs', get_file_name(u.basename(file)) }
end

local function download_image(url, output)
  os.execute(('mkdir -pv %s'):format(u.dirname(output)))
  os.execute(('curl -L -o %s %s'):format(output, url))
end

local function get_image_size(file)
  local cmd = is_video(file)
      and 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x %s'
    or 'identify -format "%%w %%h" %s | head -n1'

  local result = u.shell(cmd:format(file)) or ''
  local width, height = result:match '(%d+)[%sx](%d+)'

  return tonumber(width), tonumber(height)
end

local function set_image_size(img, file)
  local width, height = get_image_size(file)
  if width then img.attributes.width = width end
  if height then img.attributes.height = height end
end

local function process_image(input, output_base)
  local avif_output = output_base .. '.avif'
  local webp_output = output_base .. '.webp'
  local original_output = output_base .. get_file_extension(input)

  if
    u.file_exists(avif_output)
    and u.file_exists(webp_output)
    and u.file_exists(original_output)
  then
    return
  end

  local tmp_avif = path.join { tmp, images, slugify(avif_output) }
  local tmp_webp = path.join { tmp, images, slugify(webp_output) }
  local tmp_original = path.join { tmp, images, slugify(original_output) }

  os.execute(('mkdir -pv %s'):format(u.dirname(output_base)))

  if u.file_exists(tmp_avif) and u.file_exists(tmp_webp) and u.file_exists(tmp_original) then
    os.execute(('cp -v %s %s'):format(tmp_avif, avif_output))
    os.execute(('cp -v %s %s'):format(tmp_webp, webp_output))
    os.execute(('cp -v %s %s'):format(tmp_original, original_output))
    return
  end

  local width = get_image_size(input)
  local resize_opts = width > 768 and '-resize 768' or ''

  os.execute(('magick %s %s %s'):format(input, resize_opts, original_output))
  os.execute(('magick %s %s %s'):format(input, resize_opts, avif_output))
  os.execute(('magick %s -quality 80 %s %s'):format(input, resize_opts, webp_output))

  os.execute(('cp -v %s %s'):format(original_output, tmp_original))
  os.execute(('cp -v %s %s'):format(avif_output, tmp_avif))
  os.execute(('cp -v %s %s'):format(webp_output, tmp_webp))
end

local function handle_remote_image(img)
  local slug = slugify(img.src)
  local ext = get_file_extension(img.src)

  local download_path = path.join { dist, remote_images, slug .. ext }
  local tmp_path = path.join { tmp, images, slug }

  os.execute(('mkdir -pv %s'):format(u.dirname(download_path)))

  local is_exist = u.file_exists(download_path)
  local is_temp_exist = u.file_exists(tmp_path)

  if is_exist then
  -- do nothing
  elseif is_temp_exist and not is_exist then
    os.execute(('cp -v %s %s'):format(tmp_path, download_path))
  elseif not is_temp_exist then
    download_image(img.src, download_path)
    os.execute(('cp -v %s %s'):format(download_path, tmp_path))
  end

  local absolute_url = path.join { '/', remote_images, slug .. ext }
  local absolute_thumb = get_thumb_path(absolute_url)

  return absolute_url, absolute_thumb
end

local function get_image(img)
  img.attributes.loading = 'lazy'

  local absolute_url, absolute_thumb

  if is_remote_src(img.src) then
    absolute_url, absolute_thumb = handle_remote_image(img)
  else
    absolute_url = get_file_absolute_path(img.src)
    absolute_thumb = get_thumb_path(absolute_url)
  end

  local prefix = (not u.starts_with(absolute_url, '/remote_images') and src or dist)
  local input_file = prefix .. absolute_url
  local output_file = dist .. absolute_thumb

  if is_video(img.src) then img.attributes.preload = 'none' end

  if is_gif(img.src) or is_video(img.src) then
    set_image_size(img, input_file)
    img.src = absolute_url

    return img
  else
    img.attributes.alt = img.title or ''
  end

  process_image(input_file, output_file)
  set_image_size(img, output_file .. '.avif')

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
    el.text = el.text:gsub('<img.->', function(img_tag)
      local value = img_tag:match 'src="([^"]+)"'

      return action(value)
    end)
    return el
  end
end

local function get_inline_image(img, absolute_url, output_base)
  local avif_src = output_base .. '.avif'
  local webp_src = output_base .. '.webp'
  local original_src = output_base .. get_file_extension(absolute_url)

  local attrs = ''
  for k, v in pairs(img.attributes) do
    attrs = ('%s %s="%s"'):format(attrs, k, v)
  end

  local tag = [[<a href="%s">
    <picture>
      <source srcset="%s" type="image/avif" />
      <source srcset="%s" type="image/webp" />
      <img src="%s" %s />
    </picture>
  </a>]]

  return (tag):format(absolute_url, avif_src, webp_src, original_src, attrs)
end

return {
  {
    Inline = function(el)
      local function action(value)
        local temp_img = pandoc.Image({}, value)
        local img, absolute_url, output_base = get_image(temp_img)

        return get_inline_image(img, absolute_url, output_base)
      end

      return get_image_inline(el, action)
    end,
  },
  {
    Meta = function(meta)
      local function action(value)
        local temp_img = pandoc.Image({}, pandoc.utils.stringify(value))

        local img, absolute_url, output_base = get_image(temp_img)

        local avif_src = output_base .. '.avif'
        local webp_src = output_base .. '.webp'
        local original_src = output_base .. get_file_extension(absolute_url)

        return {
          url = absolute_url,
          webp = webp_src,
          avif = avif_src,
          original = original_src,
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
      local img, absolute_url, output_base = get_image(original_img)

      if is_gif(img.src) or is_video(img.src) then return img end

      local inline_img = get_inline_image(img, absolute_url, output_base)

      return pandoc.RawInline('html', inline_img)
    end,
  },
}
