vim.diagnostic.config({
  virtual_text = false, -- cleaner view
  signs = true,
  underline = true,
  update_in_insert = false,

  float = {
    border = "rounded",
    source = "always",
  },
})

-- show diagnostic popup automatically
vim.api.nvim_create_autocmd("CursorHold", {
  callback = function()
    vim.diagnostic.open_float(nil, { focusable = false })
  end
})
