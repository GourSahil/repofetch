return {
  "akinsho/toggleterm.nvim",
  version = "*",

  config = function()
    require("toggleterm").setup({
      size = 15,
      open_mapping = [[<leader>tt]],
      direction = "float",

      start_in_insert = true,
      insert_mappings = true,
      persist_size = true,
      close_on_exit = false,

      shade_terminals = false,
    })
  end,
}
