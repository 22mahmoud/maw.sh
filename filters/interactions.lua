local u = require 'filters.utils'

return {
  {
    Meta = function(meta)
      if meta['like-to'] or meta['reply-to'] then
        if meta['interaction-to-content'] then return meta end

        local url = pandoc.utils.stringify(meta['like-to'] or meta['reply-to'])
        local result = u.shell(("curl -s '%s'"):format(url))

        local e_content = pandoc.pipe('xq', { '-q', '.h-entry > .e-content' }, result)
        local u_author =
          pandoc.pipe('xq', { '-q', '.h-card > .p-name, [rel=me] > .p-name' }, result)
        local p_name =
          pandoc.pipe('xq', { '-q', '.p-name:not(.u-url.p-name, .u-url > .p-name)' }, result)

        local content = u.trim(e_content):sub(1, 100) .. '...'

        os.execute(
          string.format(
            [[yq -i --front-matter="process" ".interaction-to-content = \"%s\"" "%s"]],
            content,
            PANDOC_STATE.input_files[1]
          )
        )

        os.execute(
          string.format(
            [[yq -i --front-matter="process" ".interaction-to-title = \"%s\"" "%s"]],
            p_name,
            PANDOC_STATE.input_files[1]
          )
        )

        os.execute(
          string.format(
            [[yq -i --front-matter="process" ".interaction-to-author = \"%s\"" "%s"]],
            u_author,
            PANDOC_STATE.input_files[1]
          )
        )

        meta['interaction-to-content'] = content
        meta['interaction-to-title'] = p_name
        meta['interaction-to-author'] = u_author
      end

      return meta
    end,
  },
}
