local u = require 'filters.utils'
local path = require 'pandoc.path'

local src = 'src'
local dist = 'dist'
local tmp = '.tmp'
local remote_images = 'remote_images'
local images = 'images'
local current_file = PANDOC_STATE.input_files[1]

local function log_error(message)
  local log_path = path.join { tmp, 'image_filter_errors.log' }
  local log_file = io.open(log_path, 'a')
  if log_file then
    log_file:write(os.date '%Y-%m-%d %H:%M:%S' .. ': ' .. message .. '\n')
    log_file:close()
  end
end

local function is_remote_src(file)
  return u.starts_with(file, 'https://') or u.starts_with(file, 'http://')
end

local function get_file_absolute_path(file)
  if not path.is_relative(file) or is_remote_src(file) then return file end

  return path.normalize(path.join { '/', u.dirname(current_file):gsub('src/', ''), file })
end

local function slugify(url)
  local slugified = url:gsub('[^%w_.-]', '_')
  return slugified
end

local function get_file_extension(file)
  local _, ext = path.split_extension(file)
  return ext or '.jpg'
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
  local max_retries = 3
  local retry_delay = 2 -- seconds

  for attempt = 1, max_retries do
    os.execute(('mkdir -pv %s'):format(u.dirname(output)))

    local curl_cmd = ('curl -L -f -o %s %s'):format(output, url)
    local result = os.execute(curl_cmd)

    if result then
      return true
    else
      log_error(('Download attempt %d failed for %s'):format(attempt, url))
      os.execute(('sleep %d'):format(retry_delay))
    end
  end

  log_error(('Failed to download image after %d attempts: %s'):format(max_retries, url))
  return false
end

local function get_image_size(file)
  local cmd = is_video(file)
      and 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x %s'
    or 'magick identify -format "%%w %%h" %s | head -n1'

  local result = u.shell(cmd:format(file)) or ''
  local width, height = result:match '(%d+)[%sx](%d+)'

  return tonumber(width), tonumber(height)
end

local function set_image_size(img, file)
  local width, height = get_image_size(file)
  if width then img.attributes.width = width end
  if height then img.attributes.height = height end
end

local function process_image(input, output_base, tmp_base)
  local formats = { 'avif', 'webp', 'original' }
  local max_width = 768
  local quality = 80

  local processed_files = {}

  os.execute(('mkdir -pv %s'):format(u.dirname(output_base)))
  os.execute(('mkdir -pv %s'):format(u.dirname(tmp_base)))

  for _, format in ipairs(formats) do
    local tmp_output = format == 'original' and (tmp_base .. get_file_extension(input))
      or (tmp_base .. '.' .. format)
    local output = format == 'original' and (output_base .. get_file_extension(input))
      or (output_base .. '.' .. format)

    if u.file_exists(tmp_output) then
      os.execute(('cp -v %s %s'):format(tmp_output, output))
      table.insert(processed_files, output)
    else
      local width = get_image_size(input)
      local resize_opts = width and width > max_width and ('-resize ' .. max_width) or ''

      local cmd = format == 'avif'
          and ('magick %s %s %s && avifenc -j 4 --min 0 --max 63 -a end-usage=q -a cq-level=25 -a tune=ssim %s %s'):format(
            input,
            resize_opts,
            tmp_base .. '_tmp.' .. 'png',
            tmp_base .. '_tmp.' .. 'png',
            tmp_output
          )
        or format == 'webp' and ('magick %s  -format webp -quality %d %s %s'):format(
          input,
          quality,
          resize_opts,
          tmp_output
        )
        or ('magick %s %s %s'):format(input, resize_opts, tmp_output)

      local success, _exit_type = os.execute(cmd)

      if not success then
        log_error(('Failed to process image: %s to %s'):format(input, format))
      else
        os.execute(('cp -v %s %s'):format(tmp_output, output))
        table.insert(processed_files, output)
      end
    end
  end

  return #processed_files == #formats
end

local function handle_remote_image(img)
  local slug = slugify(img.src)
  local ext = get_file_extension(img.src)

  local download_path = path.join { dist, remote_images, slug .. ext }
  local tmp_path = path.join { tmp, images, slug .. ext }

  os.execute(('mkdir -pv %s'):format(u.dirname(download_path)))
  os.execute(('mkdir -pv %s'):format(u.dirname(tmp_path)))

  local is_exist = u.file_exists(download_path)
  local is_temp_exist = u.file_exists(tmp_path)

  if not is_exist then
    if is_temp_exist then
      os.execute(('cp -v %s %s'):format(tmp_path, download_path))
    else
      local download_success = download_image(img.src, download_path)
      if download_success then
        os.execute(('cp -v %s %s'):format(download_path, tmp_path))
      else
        return nil, nil
      end
    end
  end

  local absolute_url = path.join { '/', remote_images, slug .. ext }
  local absolute_thumb =
    path.join { u.dirname(absolute_url), 'thumbs', get_file_name(absolute_url) }

  return absolute_url, absolute_thumb
end

local function get_image(img)
  img.attributes.loading = 'lazy'

  local absolute_url, absolute_thumb

  if is_remote_src(img.src) then
    absolute_url, absolute_thumb = handle_remote_image(img)

    if not absolute_url then
      log_error('Failed to process remote image: ' .. img.src)
      return img
    end
  else
    absolute_url = get_file_absolute_path(img.src)
    absolute_thumb = get_thumb_path(absolute_url)
  end

  local prefix = (not u.starts_with(absolute_url, '/remote_images') and src or dist)
  local input_file = prefix .. absolute_url
  local tmp_thumb_base = path.join { tmp, images, get_file_name(absolute_url):gsub('^/', '') }
  local output_thumb_base = dist .. absolute_thumb

  if is_video(img.src) then img.attributes.preload = 'none' end

  if is_gif(img.src) or is_video(img.src) then
    set_image_size(img, input_file)
    img.src = absolute_url
    return img
  else
    img.attributes.alt = img.title or ''
  end

  os.execute(('mkdir -pv %s'):format(u.dirname(output_thumb_base)))

  local process_success = process_image(input_file, output_thumb_base, tmp_thumb_base)
  if not process_success then
    log_error('Image processing failed: ' .. input_file)
    return img
  end

  set_image_size(img, output_thumb_base .. '.avif')

  return img, absolute_url, absolute_thumb
end

local function get_image_meta(metadata, action)
  if type(metadata) == 'table' then
    for key, value in pairs(metadata) do
      if key == 'photo' then
        local processed_value = action(value)
        if processed_value then metadata[key] = processed_value end
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

        if not output_base then return nil end

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
