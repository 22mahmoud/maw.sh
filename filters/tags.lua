local u = require 'filters.utils'

function Meta(meta)
  if meta.template and meta.template.tags then
    for _, k in ipairs(meta['tags']) do
      local doc_meta = pandoc.Meta {}

      local files = {}

      k.entries:map(function(entry)
        table.insert(files, entry.file)
        return entry
      end)

      local collection = meta.collections[1]
      local dir = u.dirname(PANDOC_STATE.input_files[1]):gsub('^src/', '')

      doc_meta['title-prefix'] = k.key
      doc_meta['template'] = { tag = true }
      doc_meta.pagination = {
        collection = collection.key or collection.name,
        output = ('%s/%s'):format(dir, k.key),
        ['page-size'] = 30,
        ['page-path'] = 'page',
        files = files,
      }

      local doc = pandoc.Pandoc({}, doc_meta)

      u.create_html_from_doc(u.stringify(k.key), doc, '/dev/null')
    end
  end
end
