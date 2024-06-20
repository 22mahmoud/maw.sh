function os.capture(cmd, raw)
  local f = assert(io.popen(cmd, 'r'))
  local s = assert(f:read '*a')

  f:close()

  if raw then return s end

  return s:gsub('^%s+', ''):gsub('%s+$', '')
end

function Meta(m)
  if not m.date then return end

  local date = pandoc.utils.stringify(m.date)

  -- local cmd = string.format("date -d \"%s\"  '+%b %d, %Y'", date)
  local cmd = 'date -d ' .. string.format('"%s"', date) .. " '+%b %d, %Y'"
  m.formatted_date = os.capture(cmd)
  return m
end
