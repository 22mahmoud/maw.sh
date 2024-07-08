local path = require 'pandoc.path'
local u = require 'filters.utils'

function Meta(meta)
  if meta.collections then
    for _, collection in pairs(meta.collections) do
      local name = pandoc.utils.stringify(collection.name)
      local key = pandoc.utils.stringify(collection.key or collection.name)
      local has_content = pandoc.MetaBool(collection.content)
      local group_by = pandoc.utils.stringify(collection['group-by'] or '')

      local filter_by = collection['filter-by']
      local filter_by_key = pandoc.utils.stringify(filter_by and filter_by['key'] or '')
      local filter_by_value = pandoc.utils.stringify(filter_by and filter_by['value'] or '')
      local first = pandoc.utils.stringify(collection['first'] or '')
      if group_by == '' and not meta[key] then meta[key] = pandoc.MetaList {} end

      local opts = {}
      if filter_by_key ~= '' then
        opts.filter_by = { key = filter_by_key, value = filter_by_value }
      end
      if first ~= '' then opts.get_first = first end

      local files = u.get_collection_files(name, opts)

      for _, file in pairs(files) do
        local doc = pandoc.read(u.read_file(file))
        local group_by_value = group_by ~= '' and pandoc.utils.stringify(doc.meta[group_by]) or nil
        local group_by_value_type = pandoc.utils.type(doc.meta[group_by])

        if not doc.meta['title-prefix'] then doc.meta['title-prefix'] = doc.meta.date end
        doc.meta.url = path.join { '/', u.dirname(file):sub(5) }
        u.normalize_meta_relative_paths(doc.meta, doc.meta.url)
        if has_content then
          doc.meta.content = u.normalize_relative_paths(doc.blocks, doc.meta.url)
        end

        if group_by_value_type == 'List' then
          if not meta[key] then meta[key] = pandoc.MetaList {} end

          for _, value in pairs(doc.meta[group_by]) do
            local existing = meta[key]:find_if(function(obj) return obj.title == value end)

            if not existing then
              meta[key]:insert { title = value, entries = pandoc.MetaList { { doc.meta } } }
            else
              existing.entries:insert(doc.meta)
            end
          end

          goto finish
        elseif group_by_value and not meta[group_by_value] then
          meta[group_by_value] = pandoc.MetaList {}
        end

        if group_by_value then
          meta[group_by_value]:insert(doc.meta)
        else
          meta[key]:insert(doc.meta)
        end

        ::finish::
      end
    end

    return meta
  end
end
