local M = {}

function M.basename(s) return s:gsub('/$', ''):match '^.+/(.+)$' or '' end

function M.dirname(s) return s:match '(.*/)' or '' end

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

function M.filter_by(by)
  return function(xs)
    if not by then return xs end

    local out = {}
    local key = by.key
    local value = by.value

    for _, file in pairs(xs) do
      local existing = pandoc.utils.stringify(pandoc.read(M.read_file(file)).meta[key])
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

function M.get_collection_files(collection, opts)
  opts = opts or {}
  local cmd = 'find src/%s -type f -name "index.md" ! -path "src/%s/index.md"'

  return M.pipe(
    M.format(collection, collection),
    M.shell,
    M.lines_to_table,
    M.filter_by(opts.filter_by),
    M.sort_by_date,
    M.get_first(opts.get_first)
  )(cmd)
end

function M.create_html_from_doc(temp, doc, out)
  return pandoc.system.with_temporary_directory(temp, function(tmpdir)
    local src = ('%s/input.json'):format(tmpdir)

    local src_fh = io.open(src, 'w')
    src_fh:write(pandoc.write(doc, 'json'))
    src_fh:close()

    local pandoc_command = 'pandoc -d pandoc.yaml %s -f json -o %s'
    os.execute(pandoc_command:format(src, out))
    print('[html page generated]: ' .. out)
  end)
end

function M.slice(tbl, first, last, step)
  local sliced = {}

  for i = first or 1, last or #tbl, step or 1 do
    sliced[#sliced + 1] = tbl[i]
  end

  return sliced
end

return M
