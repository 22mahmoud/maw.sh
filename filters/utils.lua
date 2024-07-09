local path = require 'pandoc.path'

local M = {}

function M.find_index(xs, fn)
  for i, _ in ipairs(xs) do
    if fn(xs[i]) then return i end

    return 0
  end

  return 0
end

function M.basename(s) return path.filename(s) end

function M.dirname(s) return path.directory(s) end

function M.trim(s) return (s:gsub('^%s*(.-)%s*$', '%1')) end

function M.starts_with(str, prefix) return str:sub(1, #prefix) == prefix end

function M.strip(s) return s:match '^%s*(.-)%s*$' end

function M.stringify(value) return pandoc.utils.stringify(value or '') end

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
  table.sort(xs, function(x, y)
    local date1 = M.stringify(pandoc.read(M.read_file(x.file)).meta.date) or ''
    local date2 = M.stringify(pandoc.read(M.read_file(y.file)).meta.date) or ''
    return date1 > date2
  end)

  return xs
end

function M.lines_to_table(xs)
  local result = {}
  for line in string.gmatch(xs, '(.-)\n') do
    table.insert(result, { file = line })
  end

  return result
end

function M.filter_by(by)
  return function(xs)
    if not by then return xs end

    local out = {}
    local key = by.key
    local value = by.value

    for _, x in ipairs(xs) do
      local meta = pandoc.read(M.read_file(x.file)).meta
      local type = pandoc.utils.type(meta[key])
      local val_key = meta[key] or 'false'

      if type == 'List' then
        for _, y in ipairs(meta[key]) do
          if y == val_key then table.insert(out, x) end
        end
      elseif M.stringify(val_key) == value then
        table.insert(out, x)
      end
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

function M.group_by(by)
  return function(xs)
    if not by then return xs end

    local out = {}

    for i = 1, #xs, 1 do
      local x = xs[i]
      local meta = pandoc.read(M.read_file(x.file)).meta
      local group_by_value = meta[by]
      local group_by_value_type = pandoc.utils.type(group_by_value)

      if group_by_value_type ~= 'List' then
        local key = group_by_value
        local idx = M.find_index(out, function(x) return x.key == key end)

        local doc = { key = key, file = x.file, __done = true }

        if idx > 0 then
          table.insert(out[idx].entries, doc)
        else
          table.insert(out, {
            key = key,
            entries = { doc },
          })
        end
      else
        table.insert(out, { key = by, entries = {} })

        for _, key in ipairs(group_by_value) do
          local idx = M.find_index(out[#out], function(y) return y.key == key end)

          local doc = { key = key, type = 'list', file = x.file, __done = true }

          if idx > 0 then
            table.insert(out[#out][idx].entries, doc)
          else
            table.insert(out[#out].entries, { key = key, entries = { doc } })
          end
        end
      end
    end

    return out
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
    M.get_first(opts.get_first),
    M.group_by(opts.group_by)
  )(cmd)
end

function M.create_html_from_doc(temp, doc, out, canonical)
  return pandoc.system.with_temporary_directory(temp, function(tmpdir)
    local src = ('%s/input.json'):format(tmpdir)

    local src_fh = io.open(src, 'w')
    src_fh:write(pandoc.write(doc, 'json'))
    src_fh:close()

    local path_var, canonical_var = '', ''
    if out ~= '/dev/null' then
      local path = M.dirname(out):gsub('^dist/', '')
      path_var = path and ('--variable path=%s'):format(path) or ''
      canonical_var = canonical and ('--variable canonical=%s'):format(canonical) or ''
    end

    local pandoc_command = 'pandoc %s %s -d pandoc.yaml %s -f json -o %s'
    os.execute(pandoc_command:format(canonical_var, path_var, src, out))
    print('[html page generated]: ' .. out)
  end)
end

function M.process_collection(xs, fn)
  if xs.file then fn(xs) end

  for _, value in ipairs(xs) do
    if value.entries then
      M.process_collection(value.entries, fn)
    elseif type(value) == 'table' then
      M.process_collection(value, fn)
    end
  end
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
    local src = M.stringify(value or '')

    if not path.is_relative(src) then return end

    return path.normalize(path.join { url, src })
  end

  get_image_meta(meta, action)

  return meta
end

return M
