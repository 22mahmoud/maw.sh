function Header(el)
  if el.level == 2 then
    local id = el.identifier

    local span = pandoc.Span(el.content)
    local a = pandoc.Link({ span }, '#' .. id, '', { class = 'header-anchor' })
    local h2 = pandoc.Header(el.level, { a }, { id })

    return h2
  end
end
