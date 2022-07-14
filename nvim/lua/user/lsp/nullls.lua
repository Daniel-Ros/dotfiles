local status_ok, nullls = pcall(require, "null-ls")
if not status_ok then
  return
end

local formatter = nullls.builtins.formatting
local diagnostics = nullls.builtins.diagnostics

nullls.setup({
  sources = {
    formatter.black,
    formatter.clang_format,
  },
})


