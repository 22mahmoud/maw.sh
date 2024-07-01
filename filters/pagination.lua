local path = require 'pandoc.path'
local system = pandoc.system

local function merge_meta(original, additional)
  for k, v in pairs(additional) do
    original[k] = v
  end
  return original
end

local function read_file(file)
  local fh = io.open(file, 'r')
  if not fh then return nil end
  local content = fh:read '*a'
  fh:close()
  return content
end

local function shell(command)
  local pipe = io.popen(command, 'r')
  if not pipe then return end

  local result = pipe:read '*a'
  pipe:close()
  return result
end

local function dirname(path) return path:match '^(.*)/' end

local function get_files(dir)
  local cmd = [[find %s -type f -name "index.md" ! -path "%s/index.md"]]
  local files = shell(cmd:format(dir, dir)) .. ''

  local result = {}
  for line in string.gmatch(files, '(.-)\n') do
    table.insert(result, line)
  end

  table.sort(result, function(file1, file2)
    local date1 = pandoc.utils.stringify(pandoc.read(read_file(file1)).meta.date)
    local date2 = pandoc.utils.stringify(pandoc.read(read_file(file2)).meta.date)
    return date1 > date2
  end)

  return result
end

local function get_output_path(i, dir, page_path)
  local output_dir = 'dist/' .. dir:sub(5)

  if i == 1 then
    return output_dir .. '/index.html'
  else
    local output = ([[%s/%s/%s/index.html]]):format(output_dir, page_path, i)
    os.execute('mkdir -p ' .. dirname(output))
    return output
  end
end

local function create_html_from_doc(temp, doc, out)
  return system.with_temporary_directory(temp, function(tmpdir)
    local src = ('%s/input.json'):format(tmpdir)

    local src_fh = io.open(src, 'w')
    src_fh:write(pandoc.write(doc, 'json'))
    src_fh:close()

    local pandoc_command = 'pandoc -d pandoc.yaml %s -f json -o %s'
    os.execute(pandoc_command:format(src, out))
    print('[html page generated]: ' .. out)
  end)
end

function Meta(meta)
  if meta.pagination then
    local has_content = pandoc.MetaBool(meta.pagination['content'])
    local page_size = tonumber(pandoc.utils.stringify(meta.pagination['page-size'] or '10'))
    local page_path = pandoc.utils.stringify(meta.pagination['page-path'] or 'page')
    local collection = pandoc.utils.stringify(meta.pagination['collection'] or 'data')
    local dir = dirname(PANDOC_STATE.input_files[1])
    local tmp = path.join { '.tmp', dir }
    local files = get_files(dir)
    local total = #files
    local total_pages = math.ceil(total / page_size)

    for i = 1, total_pages do
      local has_next = i < total_pages
      local has_prev = i > 1
      local is_second = i == 2

      local next_url = has_next and path.join { '/', collection, page_path, i + 1 } or nil
      local prev_url = has_prev
          and path.join { '/', collection, is_second and '' or page_path, is_second and '' or i - 1 }
        or nil

      local additional_meta = {
        ['is-second'] = is_second,
        ['has-next'] = has_next,
        ['has-prev'] = has_prev,
        ['next-page'] = i + 1,
        ['prev-page'] = i - 1,
        ['page-path'] = page_path,
        ['prev-url'] = prev_url,
        ['next-url'] = next_url,
        [collection] = pandoc.MetaList {},
      }

      local page_meta = merge_meta(pandoc.Meta(meta), additional_meta)

      for j = 1, page_size do
        local index = (i - 1) * page_size + j
        local file = files[index]
        if not file then goto continue end
        local parent = shell(('basename %s'):format(dirname(file)))

        local doc = pandoc.read(read_file(file))

        local _meta = {
          url = '/' .. collection .. '/' .. parent,
        }

        if has_content then _meta.content = doc.blocks end

        page_meta[collection]:insert(merge_meta(pandoc.Meta(doc.meta), _meta))

        ::continue::
      end

      local doc = pandoc.Pandoc({}, page_meta)
      local output_path = get_output_path(i, dir, page_path)

      create_html_from_doc(collection, doc, output_path)
    end

    os.execute('mkdir -p ' .. tmp)
  end
end
