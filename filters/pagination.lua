local u = require 'filters.utils'
local path = require 'pandoc.path'

local function get_output_path(i, dir, page_path)
  local output_dir = 'dist/' .. dir:sub(5)

  local output = path.join { output_dir, page_path, i, 'index.php' }
  os.execute('mkdir -pv ' .. u.dirname(output))
  return output
end

local function convert_list_to_table(list)
  local out = {}

  list:map(function(x)
    table.insert(out, x)
    return x
  end)

  return out
end

function Meta(meta)
  if meta.pagination then
    local has_content = pandoc.MetaBool(meta.pagination['content'])
    local page_size = tonumber(pandoc.utils.stringify(meta.pagination['page-size'] or '10'))
    local page_path = pandoc.utils.stringify(meta.pagination['page-path'] or 'page')
    local collection = pandoc.utils.stringify(meta.pagination['collection'] or 'data')
    local output = pandoc.utils.stringify(meta.pagination['output'] or collection)
    local dir = 'src/' .. output

    local opts = {}
    if meta.pagination.cmd then opts.cmd = u.stringify(meta.pagination.cmd) end

    local files = meta.pagination.files
        and convert_list_to_table(
          meta.pagination.files:map(function(file) return { file = u.stringify(file) } end)
        )
      or u.get_collection_files(collection, opts)

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

      meta.pagination = nil
      meta['is-second'] = is_second
      meta['has-next'] = has_next
      meta['has-prev'] = has_prev
      meta['next-page'] = i + 1
      meta['prev-page'] = i - 1
      meta['page-path'] = page_path
      meta['prev-url'] = prev_url
      meta['next-url'] = next_url
      meta[collection] = pandoc.MetaList {}

      for j = 1, page_size do
        local index = (i - 1) * page_size + j
        local file = files[index] and files[index].file or nil
        if not file then goto continue end

        local doc = pandoc.read(u.read_file(file))

        doc.meta.url = path.join { '/', u.dirname(file):sub(5) }

        u.normalize_meta_relative_paths(doc.meta, doc.meta.url)

        if has_content then
          doc.meta.content = u.normalize_relative_paths(doc.blocks, doc.meta.url)
        end

        meta[collection]:insert(doc.meta)

        ::continue::
      end

      local doc = pandoc.Pandoc({}, meta)

      local output_path = get_output_path(i, dir, page_path)

      if i == 1 then
        u.create_html_from_doc(collection, doc, path.join { 'dist', dir:sub(5), 'index.html' })
        u.create_html_from_doc(collection, doc, output_path, dir:gsub('^src/', ''))
      else
        u.create_html_from_doc(collection, doc, output_path)
      end
    end
  end
end
