local path = require 'pandoc.path'

local M = {}

function M.basename(s) return path.filename(s) end

function M.dirname(s) return path.directory(s) end

function M.trim(s) return (s:gsub('^%s*(.-)%s*$', '%1')) end

function M.starts_with(str, prefix) return str:sub(1, #prefix) == prefix end

function M.shell(command)
  local pipe = io.popen(command, 'r')
  if not pipe then return end

  local result = pipe:read '*a'
  pipe:close()
  return result
end

function M.read_file(file)
  local fh = io.open(file, 'r')
  if not fh then return nil end
  local content = fh:read '*a'
  fh:close()
  return content
end

function M.file_exists(name)
  local f = io.open(name, 'r')
  if f ~= nil then
    io.close(f)
    return true
  else
    return false
  end
end

function M.slice(tbl, first, last, step)
  local sliced = {}

  for i = first or 1, last or #tbl, step or 1 do
    sliced[#sliced + 1] = tbl[i]
  end

  return sliced
end

function M.pipe(...)
  local funcs = { ... }
  return function(...)
    local args = { ... }
    for i = 1, #funcs do
      args = { funcs[i](table.unpack(args)) }
    end
    return table.unpack(args)
  end
end

function M.format(...)
  local args = { ... }
  return function(s) return string.format(s, table.unpack(args)) end
end

function M.sort_by_date(xs)
  table.sort(xs, function(file1, file2)
    local date1 = pandoc.utils.stringify(pandoc.read(M.read_file(file1)).meta.date) or ''
    local date2 = pandoc.utils.stringify(pandoc.read(M.read_file(file2)).meta.date) or ''
    return date1 > date2
  end)

  return xs
end

function M.lines_to_table(xs)
  local result = {}
  for line in string.gmatch(xs, '(.-)\n') do
    table.insert(result, line)
  end

  return result
end

function M.filter_by(by)
  return function(xs)
    if not by then return xs end

    local out = {}
    local key = by.key
    local value = by.value

    for _, file in pairs(xs) do
      local existing = pandoc.utils.stringify(pandoc.read(M.read_file(file)).meta[key] or 'false')
      if existing == value then table.insert(out, file) end
    end

    return out
  end
end

function M.get_first(x)
  return function(xs)
    if type(tonumber(x)) ~= 'number' then return xs end

    return M.slice(xs, 1, x)
  end
end

function M.get_collection_files(path, opts)
  opts = opts or {}
  local cmd = [[find src/%s -type f -name "index.md" ! -path "src/%s/index.md"]]

  return M.pipe(
    M.format(path, path),
    M.shell,
    M.lines_to_table,
    M.sort_by_date,
    M.filter_by { key = 'draft', value = 'false' },
    M.filter_by(opts.filter_by),
    M.get_first(opts.get_first)
  )(cmd)
end

function M.create_html_from_doc(temp, doc, out, canonical)
  return pandoc.system.with_temporary_directory(temp, function(tmpdir)
    local src = ('%s/input.json'):format(tmpdir)

    local src_fh = io.open(src, 'w')
    src_fh:write(pandoc.write(doc, 'json'))
    src_fh:close()

    local path = M.dirname(out):gsub('^dist/', '')
    local canonical_var = canonical and ('--variable canonical=%s'):format(canonical) or ''

    local pandoc_command = 'pandoc %s --variable path=%s -d pandoc.yaml %s -f json -o %s'
    os.execute(pandoc_command:format(canonical_var, path, src, out))
    print('[html page generated]: ' .. out)
  end)
end

local function get_image_meta(metadata, action)
  if type(metadata) == 'table' then
    for key, value in pairs(metadata) do
      if key == 'photo' then
        metadata[key] = action(value[1])
      else
        get_image_meta(value, action)
      end
    end
  end
end

function M.normalize_relative_paths(blocks, url)
  return pandoc.walk_block(pandoc.Div(blocks), {
    Image = function(image)
      if not path.is_relative(image.src) then return end

      image.src = path.normalize(path.join { url, image.src })

      return image
    end,
  }).content
end

function M.normalize_meta_relative_paths(meta, url)
  local function action(value)
    local src = pandoc.utils.stringify(value or '')

    if not path.is_relative(src) then return end

    return path.normalize(path.join { url, src })
  end

  get_image_meta(meta, action)

  return meta
end

return M
