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

  local cmd = string.format('TZ=Africa/Cairo date -d "%s" -Iseconds', date)
  m.isodate = os.capture(cmd)
  return m
end
