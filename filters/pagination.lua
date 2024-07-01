local u = require 'filters.utils'
local path = require 'pandoc.path'

local function get_output_path(i, dir, page_path)
  local output_dir = 'dist/' .. dir:sub(5)

  if i == 1 then
    return output_dir .. '/index.html'
  else
    local output = ([[%s/%s/%s/index.html]]):format(output_dir, page_path, i)
    os.execute('mkdir -p ' .. u.dirname(output))
    return output
  end
end

function Meta(meta)
  if meta.pagination then
    local has_content = pandoc.MetaBool(meta.pagination['content'])
    local page_size = tonumber(pandoc.utils.stringify(meta.pagination['page-size'] or '10'))
    local page_path = pandoc.utils.stringify(meta.pagination['page-path'] or 'page')
    local collection = pandoc.utils.stringify(meta.pagination['collection'] or 'data')
    local dir = u.dirname(PANDOC_STATE.input_files[1])
    local tmp = path.join { '.tmp', dir }
    local files = u.get_collection_files(u.basename(dir))
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
        local file = files[index]
        if not file then goto continue end
        local parent = u.basename(u.dirname(file))

        local doc = pandoc.read(u.read_file(file))

        doc.meta.url = ('/%s/%s'):format(collection, parent)
        if has_content then doc.meta.content = doc.blocks end

        meta[collection]:insert(doc.meta)

        ::continue::
      end

      local doc = pandoc.Pandoc({}, meta)
      local output_path = get_output_path(i, dir, page_path)

      u.create_html_from_doc(collection, doc, output_path)
    end

    os.execute('mkdir -p ' .. tmp)
  end
end
