local path = require 'pandoc.path'
local u = require 'filters.utils'

function Meta(meta)
  if meta.collections then
    for _, collection in pairs(meta.collections) do
      local name = u.stringify(collection.name)
      local has_content = pandoc.MetaBool(collection.content)
      local group_by = u.stringify(collection['group-by'] or '')

      local filter_by = collection['filter-by']
      local filter_by_key = u.stringify(filter_by and filter_by['key'] or '')
      local filter_by_value = u.stringify(filter_by and filter_by['value'] or '')
      local first = u.stringify(collection['first'] or '')

      local opts = {}
      if filter_by_key ~= '' then
        opts.filter_by = { key = filter_by_key, value = filter_by_value }
      end

      if group_by ~= '' then opts.group_by = group_by end
      if first ~= '' then opts.get_first = first end

      if collection.cmd then opts.cmd = u.stringify(collection.cmd) end

      local files = u.get_collection_files(name, opts)

      u.process_collection(files, function(x)
        local file, type, i = x.file, x.type, u.stringify(x.key)
        local k = u.stringify(collection.key or x.key or collection.name)

        local doc = pandoc.read(u.read_file(file))

        if not doc.meta['title-prefix'] then doc.meta['title-prefix'] = doc.meta.date end

        doc.meta.url = path.join { '/', u.dirname(file):sub(5) }
        doc.meta.file = file

        u.normalize_meta_relative_paths(doc.meta, doc.meta.url)

        if has_content then
          doc.meta.content = u.normalize_relative_paths(doc.blocks, doc.meta.url)
        end

        if type ~= 'list' then
          meta[k] = meta[k] or pandoc.MetaList {}
          meta[k]:insert(doc.meta)
        else
          meta[k] = meta[k] or pandoc.MetaList {}
          local existing = meta[k]:find_if(function(x) return x.key == i end)

          if not existing then
            meta[k]:insert { key = i, entries = pandoc.MetaList { doc.meta } }
          else
            existing.entries:insert(doc.meta)
          end
        end
      end)
    end
  end

  return meta
end
