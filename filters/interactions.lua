local function trim(s) return (s:gsub('^%s*(.-)%s*$', '%1')) end

return {
  {
    Meta = function(meta)
      if meta['like-to'] or meta['reply-to'] then
        if meta['interaction-to-content'] then return meta end

        local url = pandoc.utils.stringify(meta['like-to'])
        local cmd = string.format('curl -s %s | htmlq --text ".e-content"', url)

        local handle = io.popen(cmd)

        if not handle then return nil, nil end

        local result = handle:read '*a'
        handle:close()

        local content = trim(result):sub(1, 100) .. '...'

        os.execute(
          string.format(
            [[yq -i --front-matter="process" ".interaction-to-content = \"%s\"" "%s"]],
            content,
            PANDOC_STATE.input_files[1]
          )
        )

        meta['interaction-to-content'] = content
      end

      return meta
    end,
  },
}
