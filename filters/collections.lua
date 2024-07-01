local u = require 'filters.utils'

function Meta(meta)
  if meta.collections then
    for _, collection in pairs(meta.collections) do
      local name = pandoc.utils.stringify(collection.name)
      local key = pandoc.utils.stringify(collection.key or collection.name)
      local has_content = pandoc.MetaBool(collection.content)
      local groupBy = pandoc.utils.stringify(collection['group-by'] or '')

      if groupBy == '' then meta[key] = pandoc.MetaList {} end

      local filterBy = collection['filter-by']
      local filterByKey = pandoc.utils.stringify(filterBy and filterBy['key'] or '')
      local filterByValue = pandoc.utils.stringify(filterBy and filterBy['value'] or '')
      local first = pandoc.utils.stringify(collection['first'] or '')

      local opts = {}
      if filterByKey ~= '' then opts.filter_by = { key = filterByKey, value = filterByValue } end
      if first ~= '' then opts.get_first = first end

      local files = u.get_collection_files(name, opts)

      for _, file in pairs(files) do
        local doc = pandoc.read(u.read_file(file))
        local groupValue = groupBy ~= '' and pandoc.utils.stringify(doc.meta[groupBy]) or nil

        if groupValue and not meta[groupValue] then meta[groupValue] = pandoc.MetaList {} end

        doc.meta.url = u.dirname(file):sub(5)
        if has_content then doc.meta.content = doc.blocks end

        if groupValue then
          meta[groupValue]:insert(doc.meta)
        else
          meta[key]:insert(doc.meta)
        end
      end
    end

    return meta
  end
end
