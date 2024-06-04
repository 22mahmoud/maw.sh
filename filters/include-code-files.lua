--- include-code-files.lua – filter to include code from source files
---
--- Copyright: © 2020 Bruno BEAUFILS
--- License:   MIT – see LICENSE file for details

local path = require 'pandoc.path'

--- Dedent a line
local function dedent(line, n) return line:sub(1, n):gsub(' ', '') .. line:sub(n + 1) end

local function get_absolute_path(file)
  local current_file_dir = string.match(PANDOC_STATE.input_files[1], '(.*/)')
  return path.join { current_file_dir, file }
end

--- Filter function for code blocks
local function transclude(cb)
  if cb.attributes.include then
    local content = ''
    local include_path = get_absolute_path(cb.attributes.include)
    local fh = io.open(include_path)
    if not fh then
      io.stderr:write('Cannot open file ' .. include_path .. ' | Skipping includes\n')
    else
      local number = 1
      local start = 1

      -- change hyphenated attributes to PascalCase
      for i, pascal in pairs { 'startLine', 'endLine' } do
        local hyphen = pascal:gsub('%u', '-%0'):lower()
        if cb.attributes[hyphen] then
          cb.attributes[pascal] = cb.attributes[hyphen]
          cb.attributes[hyphen] = nil
        end
      end

      if cb.attributes.startLine then
        cb.attributes.startFrom = cb.attributes.startLine
        start = tonumber(cb.attributes.startLine)
      end
      for line in fh:lines 'L' do
        if cb.attributes.dedent then line = dedent(line, cb.attributes.dedent) end
        if number >= start then
          if not cb.attributes.endLine or number <= tonumber(cb.attributes.endLine) then
            content = content .. line
          end
        end
        number = number + 1
      end
      fh:close()
    end
    -- remove key-value pair for used keys
    cb.attributes.include = nil
    cb.attributes.startLine = nil
    cb.attributes.endLine = nil
    cb.attributes.dedent = nil
    -- return final code block
    return pandoc.CodeBlock(content, cb.attr)
  end
end

return {
  { CodeBlock = transclude },
}
