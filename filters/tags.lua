local u = require 'filters.utils'
local path = require 'pandoc.path'

local function get_output_path(i, dir, page_path)
  local output_dir = 'dist/' .. dir:sub(5)

  local output = path.join { output_dir, page_path, i, 'index.html' }
  os.execute('mkdir -pv ' .. u.dirname(output))
  return output
end

function Meta(meta)
  if meta['tags-page'] then
    for _, k in ipairs(meta['tags']) do
      local doc_meta = pandoc.Meta {}
      doc_meta['title-prefix'] = k.key

      local collection = meta.collections[1]
      doc_meta['tag-page'] = true
      doc_meta.pagination = {
        collection = collection.name,
        output = 'tags/' .. k.key,
        ['page-size'] = 30,
        ['page-path'] = 'page',
        ['filter-by'] = {
          key = collection['group-by'],
          value = k.key,
        },
      }

      local doc = pandoc.Pandoc({}, doc_meta)

      u.create_html_from_doc(u.stringify(collection), doc, '/dev/null')
    end
  end
end
