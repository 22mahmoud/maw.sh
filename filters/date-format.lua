function os.capture(cmd, raw)
  local f = assert(io.popen(cmd, 'r'))
  local s = assert(f:read '*a')

  f:close()

  if raw then return s end

  return s:gsub('^%s+', ''):gsub('%s+$', '')
end

local function find_date_metadata(metadata, action)
  if type(metadata) == 'table' then
    for key, value in pairs(metadata) do
      if key == 'date' then
        metadata['formatted_date'] = action(value)
      else
        find_date_metadata(value, action)
      end
    end
  end
end

local function action(value)
  local date = pandoc.utils.stringify(value)

  -- local cmd = string.format("date -d \"%s\"  '+%b %d, %Y'", date)
  local cmd = 'date -d ' .. string.format('"%s"', date) .. " '+%b %d, %Y'"
  return os.capture(cmd)
end

function Meta(metadata)
  find_date_metadata(metadata, action)
  return metadata
end
